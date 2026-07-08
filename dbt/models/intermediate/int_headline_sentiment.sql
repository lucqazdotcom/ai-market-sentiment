-- NOTE: get the sentiment intensity per topic, per week - average sum
-- grain: week
with
source as (
    select
        *
    from {{ref('stg_newsapi_headlines')}}
)

select
    sum(cast(sentiment_compound_score as float64)) as weekly_sentiment_intensity,
    source_name,
    signal_topic,
    date_trunc(CAST(publish_date as timestamp), week) as week_start_date
from source
group by
source.source_name,
source.signal_topic,
week_start_date
