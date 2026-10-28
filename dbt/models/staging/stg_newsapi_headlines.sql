with
    observed_headlines as (
        select
            *,
            row_number() over (
                partition by url, signal_topic order by insert_date desc

            ) as observation_rank

        from {{ source("raw", "headlines") }}
        where signal_topic is not null and url is not null
    )

select * except (observation_rank)
from observed_headlines
where observation_rank = 1
