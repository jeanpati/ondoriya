{{ config(materialized='view') }}

SELECT faction,
       percent
FROM {{ ref('faction_distribution') }}
WHERE faction != 'Total'
ORDER BY CAST(REPLACE(percent, '%', '') AS DOUBLE) DESC
LIMIT 1
