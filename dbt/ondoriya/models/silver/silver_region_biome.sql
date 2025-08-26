{{ config(materialized='incremental',
    pre_hook=[
        "SET s3_endpoint='localhost:9000'",
        "SET s3_use_ssl=false", 
        "SET s3_access_key_id='admin'",
        "SET s3_secret_access_key='password'",
        "SET s3_url_style='path'"
    ]
) }}

SELECT 
"Region_ID" as region_id,
"Full_Name" as full_name,
"Biome" as biome
FROM read_parquet('s3://bronze/region_biome.parquet')