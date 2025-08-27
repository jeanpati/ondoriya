import os
import requests
from dotenv import load_dotenv
from minio import Minio
from utils.logger import setup_logger
import pandas as pd
from io import BytesIO
import urllib3

load_dotenv()

logger = setup_logger(__name__, "./logs/ingest.log")


MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_URL = os.getenv("MINIO_URL")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")


BASE_URL = "https://sample.ondoriya.com"


FILES_TO_INGEST = [
    "faction_distribution.csv",
    "households.csv",
    "language_building_blocks.csv",
    "language_roots.csv",
    "moons.csv",
    "people.csv",
    "planets.csv",
    "region_biome.csv",
    "regions.csv",
]


def main():
    """
    Connects to MinIO, downloads files from a public URL,
    and uploads them to a MinIO bucket.
    """
    http_client = urllib3.PoolManager(
        cert_reqs="CERT_NONE",
    )
    minio_client = Minio(
        MINIO_URL,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
        http_client=http_client,
    )

    if not minio_client.bucket_exists(MINIO_BUCKET):
        minio_client.make_bucket(MINIO_BUCKET)
        logger.info("Created bucket: %s", MINIO_BUCKET)
    else:
        logger.info("Bucket %s already exists", MINIO_BUCKET)

    for file in FILES_TO_INGEST:
        file_url = f"{BASE_URL}/{file}"
        response = requests.get(file_url, timeout=(30, 60))
        response.raise_for_status()

        csv_dataframe = pd.read_csv(BytesIO(response.content))
        parquet_buffer = BytesIO()
        csv_dataframe.to_parquet(parquet_buffer, index=False)

        file_name = file.replace(".csv", ".parquet")
        file_data = parquet_buffer.getvalue()
        file_size = len(file_data)
        file_data_buffer = BytesIO(file_data)

        minio_client.put_object(
            MINIO_BUCKET,
            file_name,
            file_data_buffer,
            file_size,
        )
        print(f"   -> Successfully uploaded {file_name}.")


if __name__ == "__main__":
    main()
