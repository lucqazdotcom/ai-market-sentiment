-- NOTE: polarity direction per topic per headline
-- grain: per headline
select
    date_trunc(CAST(p.publish_date as timestamp), week) as week_start_date,
    p.title,
    p.signal_topic,
    p.sentiment_compound_score,
    t.polarity,
    t.polarity * ABS(CAST(p.sentiment_compound_score as float64)) as directional_score
from {{ref('stg_newsapi_headlines')}} p
left join {{ref('signal_topic_polarity')}} t
on p.signal_topic = t.signal_topic
