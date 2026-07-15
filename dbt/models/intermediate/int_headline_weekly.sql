-- NOTE: Directional score per topic per week
-- grain: week
SELECT
    week_start_date,
    signal_topic,
    count(title) as total_headlines,
    sum(directional_score) as directional_score_total
from {{ref('int_headline_signal')}}
group by
week_start_date,
signal_topic
