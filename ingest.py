import os
import requests
from dotenv import load_dotenv
from minio import Minio
from utils.logger import setup_logger

load_dotenv()

logger = setup_logger(__name__, "./logs/ingest.log")


MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_URL_HOST_PORT = os.getenv("MINIO_EXTERNAL_URL")
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
    # 1. Initialize MinIO client make sure you have a bucket you want to use.
    minio_client = Minio(
        MINIO_URL_HOST_PORT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )

    # 2. Download Files

    file_url = f"{BASE_URL}/planets.csv"
    # Here is an example of how to get one of the files
    response = requests.get(file_url)
    response.raise_for_status()  # Raise an exception for bad status codes

    # 3.  Upload the file data to MinIO

    # minio_client.put_object(
    #     MINIO_BUCKET, filename, file_data, file_size  # The object name in the bucket
    # )
    # print(f"   -> Successfully uploaded {filename}.")


if __name__ == "__main__":
    main()
