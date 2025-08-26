{{ config(materialized='view') }}

SELECT COUNT(*) AS total_population FROM {{ ref('people') }}) 