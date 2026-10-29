-- NOTE: collect weekly job inventory posting by company
-- grain: week
with
    daily_inventory as (
        select
            date_posted,
            company,
            sum(count) as daily_visible_roles,
            count(distinct search_term) as search_terms_tracked
        from {{ ref("stg_adzuna_job_inventory") }}
        group by date_posted, company
    )
select
    date_trunc(date_posted, week) as week_start_date,
    company,
    avg(daily_visible_roles) as total_visible_roles,
    avg(search_terms_tracked) as search_terms_tracked,
    count(*) as days_observed
from daily_inventory
group by week_start_date, company
