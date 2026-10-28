import os

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()


def get_client():
    return bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))


def write_to_big_query(
    data: list,
    dataset: str,
    table: str,
    schema: list[bigquery.SchemaField],
    batch_size: int = 500,
):
    client = get_client()
    table_ref = f"{os.getenv('GCP_PROJECT_ID')}.{dataset}.{table}"
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
    )

    for i in range(0, len(data), batch_size):
        job = client.load_table_from_json(
            data[i : i + batch_size], table_ref, job_config=job_config
        )
        job.result()

    print(f"inserted {len(data)} rows into {table_ref}")
