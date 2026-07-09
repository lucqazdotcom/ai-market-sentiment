--NOTE: Delta between job volume by company and media narrative score by topic
-- grain: week
-- (tw - lw) / lw

with

job_inventory as (
    select
        week_start_date,
        company,
        total_visible_roles as current_role_inventory,
        lag(total_visible_roles) over(partition by company order by week_start_date) as previous_role_inventory,
        round(
        (total_visible_roles - lag(total_visible_roles) over(partition by company order by week_start_date)) /
        nullif(lag(total_visible_roles) over(partition by company order by week_start_date), 0) * 100
        , 2) as delta
    from {{ref('int_company_daily_job_inventory')}}
),

headline_intensity as (
    select
        week_start_date,
        weekly_sentiment_score as current_sentiment_score,
        lag(weekly_sentiment_score) over(order by week_start_date) as previous_sentiment_score,
        round(
        (weekly_sentiment_score - lag(weekly_sentiment_score) over(order by week_start_date)) /
        nullif(lag(weekly_sentiment_score) over(order by week_start_date), 0) * 100
        , 2) as delta
    from {{ref('int_headline_sentiment_total')}}
)

select
    p.week_start_date,
    p.current_role_inventory,
    p.delta as inventory_delta,
    t.current_sentiment_score,
    t.delta as sentiment_delta
from job_inventory p
left join headline_intensity t
on t.week_start_date = p.week_start_date
