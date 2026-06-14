import requests
from dotenv import load_dotenv
import os

from company_aliases import COMPANIES
from ingestion.utils.bq_client import insert_rows

load_dotenv()

query_params = {
    "apiKey": os.getenv("NEWSAPI_KEY"),
    "from": "2026-06-01",
    "languages": "en",
    "sortBy": "popularity",
}


def run_scraper():
    BASE_URL = "https://newsapi.org/v2/everything?"

    for company, query_string in COMPANIES.items():
        data = get_articles(BASE_URL, company, query_string)
        write_to_bq(data)


def get_articles(url: str, company: str, query_string: str) -> object:
    params = {**query_params, "q": query_string}
    response = requests.get(url, params=params).json()
    articles = response.get("articles")
    cleaned_articles = []
    target_keys = ("source-id", "source-name", "author", "title",
                   "description", "url", "publish-date", "content", "company")
    for article in articles:
        article["source-id"] = article.get("source", {}).get("id")
        article["source-name"] = article.get("source", {}).get("name")
        article["publish-date"] = article.get("publishedAt")
        article["company"] = company
        cleaned_articles.append({k: article.get(k) for k in target_keys})

    return cleaned_articles


def write_to_bq(data: list, batch_size: int = 500) -> None:
    for i in range(0, len(data), batch_size):
        insert_rows(data[i:i + batch_size], "raw", "headlines")
