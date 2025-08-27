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
"World_ID" as world_id,
"World_Name" as world_name,
"Star_System" as star_system,
"Planet_Type" as planet_type,
"Gravity_g" as gravity_g,
"Day_Length_hours" as day_length_hours,
"Year_Length_days" as year_length_days,
"Axial_Tilt_deg" as axial_tilt_deg,
"Calendar_Name" as calendar_name
 FROM read_parquet('s3://bronze/planets.parquet')