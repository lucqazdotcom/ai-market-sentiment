-- NOTE: Net score total per week
-- grain: week
SELECT
    week_start_date,
    sum(directional_score_total) as net_displacement_score
from {{ref('int_headline_weekly')}}
group by
week_start_date
order by 1
