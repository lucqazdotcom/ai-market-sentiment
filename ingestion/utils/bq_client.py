from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()


def get_client():
    return bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))


def insert_rows(dataset: str, table: str, rows: list):
    client = get_client()
    table_ref = f"{os.getenv('GCP_PROJECT_ID')}.{dataset}.{table}"

    job = client.load_table_from_json(rows, table_ref)
    job.result()

    print(f"inserted {len(rows)} rows into {table_ref}")



def run_query(sql: str):
    client = get_client()
    return client.query(sql).to_dataframe()
