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
    "Language_ID" as language_id,
    "Language_Name" as language_name,
    "Branch_From" as branch_from,
    "Phonology_Notes" as phonology_notes,
    "Morphology_Patterns" as morphology_patterns,
    "Example_Roots" as example_roots
FROM read_parquet('s3://bronze/language_building_blocks.parquet')