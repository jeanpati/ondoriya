{{ config(materialized='table',
    pre_hook=[
        "SET s3_endpoint='localhost:9000'",
        "SET s3_use_ssl=false", 
        "SET s3_access_key_id='admin'",
        "SET s3_secret_access_key='password'",
        "SET s3_url_style='path'"
    ]
) }}

SELECT 
    "Moon_ID" as moon_id,
    "Moon_Name" as moon_name,
    "Settlement_Formal" as settlement_formal,
    "Colloquial" as colloquial,
    "Staff_Size" as staff_size,
    "Specialty" as specialty,
    "Language_Origin" as language_origin
 FROM read_parquet('s3://bronze/moons.parquet')