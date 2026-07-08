select
    date_trunc(CAST(date as timestamp), week) as week_start_date,
    company,
    sum(count) as total_visible_roles,
    count(distinct search_term) as search_terms_tracked,
from {{ref('stg_adzuna_job_inventory')}}
group by
    week_start_date,
    company

