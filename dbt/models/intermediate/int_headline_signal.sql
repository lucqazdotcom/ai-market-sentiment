-- NOTE: polarity direction per topic per headline
-- grain: week
select
    p.week_start_date,
    p.title,
    p.signal_topic,
    p.sentiment_compound_score,
    t.polarity,
    t.polarity * ABS(p.sentiment_compound_score) as derived_score
from {{ref('stg_news_api_headlines')}} p
left join {{ref('signal_topic_polarity')}} t
on p.signal_topic = t.signal_topic
