import requests
from dotenv import load_dotenv
import os
from company_aliases import COMPANIES, ROLES
from ingestion.utils.bq_client import write_to_big_query

load_dotenv()

BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"
base_query_params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "api_key": os.getenv("ADZUNA_API_KEY"),
    "country": "us",
    "page_number": 1,
    "results_per_page": 50,
    "sort_by": "date",
    "content-type": "application/json",
    "company_name": "",
    "what": ""
}
search_candidates = []


def run_job_scrapper():


def get_open_roles(url: str) -> object:
    for i in search_candidates:
        params = {
            **base_query_params,
            "company_name": i.get("company_search_term"),
            "what": i.get("role_search_term")
        }

        response = requests.get(f"{BASE_URL}?{params}")


def create_search_candidate():
    for company, alias in COMPANIES.items():
        for role_type, role_name in ROLES.items():
            search_candidates.append({
                "company_name": company,
                "company_search_term": alias,
                "role_type": role_type,
                "role_search_term": role_name
            })


def query_roles() -> str:
