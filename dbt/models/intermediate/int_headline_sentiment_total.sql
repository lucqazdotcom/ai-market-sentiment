-- NOTE: get the sentiment intensity accross all topics per week - average sum
-- grain: week
select
    date_trunc(CAST(publish_date as timestamp), week) as week_start_date,
    sum(cast(sentiment_compound_score as float64)) as weekly_sentiment_score,
from {{ref('stg_newsapi_headlines')}}
group by week_start_date
