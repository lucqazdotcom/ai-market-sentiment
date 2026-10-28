from google.cloud import bigquery

HEADLINES_SCHEMA = [
    bigquery.SchemaField("id", "STRING"),
    bigquery.SchemaField("source_id", "STRING"),
    bigquery.SchemaField("source_name", "STRING"),
    bigquery.SchemaField("author", "STRING"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("url", "STRING"),
    bigquery.SchemaField("publish_date", "TIMESTAMP"),
    bigquery.SchemaField("insert_date", "TIMESTAMP"),
    bigquery.SchemaField("content", "STRING"),
    bigquery.SchemaField("signal_topic", "STRING"),
    bigquery.SchemaField("search_query", "STRING"),
    bigquery.SchemaField("sentiment_compound_score", "FLOAT64"),
    bigquery.SchemaField("sentiment_divergence", "FLOAT64"),
]

JOB_INVENTORY_SCHEMA = [
    bigquery.SchemaField("count", "INT64"),
    bigquery.SchemaField("company", "STRING"),
    bigquery.SchemaField("role_group", "STRING"),
    bigquery.SchemaField("search_term", "STRING"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("source", "STRING"),
    bigquery.SchemaField("date_posted", "DATE"),
    bigquery.SchemaField("run_timestamp", "TIMESTAMP"),
]
