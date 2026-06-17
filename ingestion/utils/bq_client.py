from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()


def get_client():
    return bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))


def write_to_big_query(data: list, dataset: str, table: str, batch_size: int = 500):
    client = get_client()
    table_ref = f"{os.getenv('GCP_PROJECT_ID')}.{dataset}.{table}"

    for i in range(0, len(data), batch_size):
        job = client.load_table_from_json(data[i:i + batch_size], table_ref)
        job.result()

    print(f"inserted {len(data)} rows into {table_ref}")


def run_query(sql: str):
    client = get_client()
    return client.query(sql).to_dataframe()
