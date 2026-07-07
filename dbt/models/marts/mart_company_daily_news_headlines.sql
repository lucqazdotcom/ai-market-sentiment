select
    format_timestamp('%Y/%m/%d', CAST(publish_date as timestamp)) as publish_date,
    source_name,
    signal_topic,
    sentiment_compound_score,
    sentiment_divergence
from {{ref('stg_newsapi_headlines')}}


