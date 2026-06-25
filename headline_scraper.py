import requests
from dotenv import load_dotenv
import os

from constants.companies import COMPANIES
from constants.news_keywords import NEWS_NARRATIVE_KEYWORDS
from ingestion.utils.bq_client import write_to_big_query

load_dotenv()

query_params = {
    "apiKey": os.getenv("NEWSAPI_KEY"),
    "from": "2026-06-01",
    "languages": "en",
    "sortBy": "popularity",
}


def run_headline_scraper():
    BASE_URL = "https://newsapi.org/v2/everything?"

    for company in COMPANIES.values():
        for query_group, query_string in NEWS_NARRATIVE_KEYWORDS.items():
            data = get_articles(BASE_URL, company, query_group, query_string)
            write_to_big_query(data, "raw", "headlines")


def get_articles(url: str, company: str, query_group: str, query_string: str) -> object:
    params = {**query_params, "q": query_string}
    response = requests.get(url, params=params).json()
    articles = response.get("articles")
    cleaned_articles = []
    target_keys = ("source-id", "source-name", "author", "title",
                   "description", "url", "publish-date", "content", "company",
                   "keyword_group", "keyword_string")
    for article in articles:
        article["source-id"] = article.get("source", {}).get("id")
        article["source-name"] = article.get("source", {}).get("name")
        article["publish-date"] = article.get("publishedAt")
        article["company"] = company
        article["keyword_group"] = query_group
        article["keyword_string"] = query_string
        cleaned_articles.append({k: article.get(k) for k in target_keys})

    return cleaned_articles
