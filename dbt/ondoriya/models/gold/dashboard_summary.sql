{{ config(materialized='table') }}

WITH population_by_region AS (
    SELECT
        r.region_id,
        r.full_name,
        COUNT(pe.person_id) AS population_count
    FROM {{ ref('regions') }} r
    LEFT JOIN {{ ref('households') }} h ON r.region_id = h.region_id
    LEFT JOIN {{ ref('people') }} pe ON h.household_id = pe.household_id
    GROUP BY r.region_id, r.full_name
)
SELECT

    pbr.full_name as region_full_name,
    pbr.population_count AS region_population_density,
    r.colloquial_name,
    r.current_faction,
    r.primary_industry,
    r.density_tier,
    r.vote_history_last3,

    RANK() OVER (ORDER BY pbr.population_count DESC) AS rank_by_population

FROM population_by_region pbr
JOIN {{ ref('regions') }} r ON r.region_id = pbr.region_id
JOIN {{ ref('faction_distribution') }} f ON f.faction = r.current_faction
ORDER BY pbr.population_count DESC