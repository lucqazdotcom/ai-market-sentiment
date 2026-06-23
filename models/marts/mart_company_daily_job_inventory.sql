select
    date as day_ran,
    company,
    sum(count) as total_visible_roles,
    count(distinct search_term) as search_terms_tracked,
    min(run_timestamp) as first_observed,
    max(run_timestamp) as last_observed,
from {{ref('stg_adzuna_job_inventory')}}
group by
    day_ran,
    company

