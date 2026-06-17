import requests
from dotenv import load_dotenv
import os

load_dotenv()

query_params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "api_key": os.getenv("ADZUNA_API_KEY"),
    "country": "us",
    "page_number": 1,
    "results_per_page": 50,
    "sort_by": "date",
    "content-type": "application/json"
}


def run_job_scrapper():
    BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"


def get_open_roles():

