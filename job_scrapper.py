import requests
import os
import time
from dotenv import load_dotenv
from datetime import datetime
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


def run_job_scrapper():
    create_search_candidate()
    # print(len(search_candidates))
    get_open_roles(BASE_URL, search_candidates)


def get_open_roles(url: str, search_input: list):
    job_inventory = []
    for i, search in enumerate(search_input):
        params = {
            **base_query_params,
            "company": search.get("company_search_term"),
            "title_only": search.get("role_search_term")
        }

        response = requests.get(BASE_URL, params=params).json()
        print(response.get("count"))
        job_inventory.append({
            "count": response.get("count"),
            "company": search.get("company_name"),
            "role_group": search.get("role_group"),
            "search_term": search.get("role_search_term"),
            "country": "us",
            "source": "adzuna",
            "created_at": datetime.now(),
        })

        # NOTE: Adzuna rate limit @ 25 hits/ min - below is a helper
        if (i + 1) % 25 == 0:
            print(job_inventory)
            time.sleep(60)


def create_search_candidate():
    for company, alias in COMPANIES.items():
        for role_group, roles in ROLES.items():
            for role_name in roles:
                search_candidates.append({
                    "company_name": company,
                    "company_search_term": alias,
                    "role_group": role_group,
                    "role_search_term": role_name
                })
