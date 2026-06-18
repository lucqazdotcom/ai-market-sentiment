import requests
from dotenv import load_dotenv
import os
from company_aliases import COMPANIES, ROLES
from ingestion.utils.bq_client import write_to_big_query

load_dotenv()

BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"
base_query_params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "app_key": os.getenv("ADZUNA_API_KEY"),
    "results_per_page": 50,
    "sort_by": "date",
    "company": "",
    "title_only": ""
    # "country": "us",
    # "page_number": 1,
}
search_candidates = []
job_postings = []


def run_job_scrapper():
    create_search_candidate()
    get_open_roles(BASE_URL)


def get_open_roles(url: str):
    for i in range(len(search_candidates) + 1):
        params = {
            **base_query_params,
            "company": search_candidates[i].get("company_search_term"),
            "title_only": search_candidates[i].get("role_search_term")
        }

        # print(params)
        print(f"{BASE_URL}?{params}")

        response = requests.get(BASE_URL, params=params)
        print(response)

        if i > 1:
            break


def create_search_candidate():
    for company, alias in COMPANIES.items():
        for role_name in ROLES:
            search_candidates.append({
                "company_name": company,
                "company_search_term": alias,
                "role_search_term": role_name
            })


# def query_roles() -> str:
