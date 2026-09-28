-- NOTE: Market contradiction between job inventory and narrative trends
-- grain: week
with
t_weekly_jobs as (
    select
        week_start_date,
        sum(total_visible_roles) as total_visible_roles
    from {{ref('int_company_postings_weekly')}}
    group by week_start_date
),

weekly_directional_score as (
    select
        week_start_date,
        sum(directional_score_total) as narrative_directional_score
    from {{ref('int_headline_weekly')}}
    group by week_start_date
)

SELECT
    coalesce(p.week_start_date, t.week_start_date) as week_start_date,
    p.total_visible_roles,
    round(
        (p.total_visible_roles - lag(p.total_visible_roles) over(order by p.week_start_date)) /
                nullif(lag(p.total_visible_roles) over(order by p.week_start_date), 0)
                * 100
            ,2) as visible_roles_delta,
    t.narrative_directional_score,
    round(
        (t.narrative_directional_score - lag(t.narrative_directional_score) over(order by t.week_start_date)) /
                nullif(lag(t.narrative_directional_score) over(order by t.week_start_date), 0)
                * 100
            ,2) as narrative_directional_score_delta,
from t_weekly_jobs p
full outer join weekly_directional_score t
on p.week_start_date = t.week_start_date
order by 1
