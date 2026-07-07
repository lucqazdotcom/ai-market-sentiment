with
source as (
    select
        *
    from {{ref('stg_newsapi_headlines')}}
),


