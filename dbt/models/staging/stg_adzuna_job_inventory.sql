with
    observed_jobs as (
        select
            *,
            row_number() over (
                partition by
                    source, country, company, role_group, search_term, date_posted
                order by run_timestamp desc

            ) as observation_rank

        from {{ source("raw", "job_inventory") }}
        where count is not null
    )

select * except (observation_rank)
from observed_jobs
where observation_rank = 1
