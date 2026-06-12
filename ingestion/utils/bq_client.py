from google.cloud import bigquery
import os


def get_client():
    return bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
