--NOTE: Delta between job volume by company and media narrative score by topic
-- grain: week
-- (tw - lw) / lw

with

job_inventory as (
    week_start_date,
    total_visible_roles,
    lag(total_visible_roles) over(order by week_start_date) as previous_week,
)
