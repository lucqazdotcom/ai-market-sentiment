import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from constants.news_keywords import TRUSTED_DOMAINS, SIGNAL_TOPICS
from ingestion.utils.bq_client import write_to_big_query
from sentiment_analysis import analyze

load_dotenv()

query_params = {
    "apiKey": os.getenv("NEWSAPI_KEY"),
    "from": "2026-06-01",
    "domains": TRUSTED_DOMAINS,
    "languages": "en",
    "sortBy": "popularity",
}


def run_headline_scraper():
    BASE_URL = "https://newsapi.org/v2/everything?"

    query_group = build_query()

    for query_obj in query_group:

        stop = 0
        while stop < 3:
            data = get_articles(BASE_URL, query_obj)
            print(data[stop].get("title"))
            analyze(data[stop].get("title"))
            stop+=1

        # write_to_big_query(data, "raw", "headlines")


def build_query() -> list:
    query_groups = []

    for group, targets in SIGNAL_TOPICS.items():
        query_groups.append({
            "signal_topic": group,
            "query_string": " OR ".join(f"({phrase})" for phrase in targets["match_units"])
        })

    return query_groups


def get_articles(url: str, query_obj: object) -> object:
    params = {**query_params, "q": query_obj.get("query_string")}
    response = requests.get(url, params=params).json()
    articles = response.get("articles")
    cleaned_articles = []
    target_keys = ("source_id", "source_name", "author", "title",
                   "description", "url", "publish_date", "insert_date",
                   "content", "signal_topic", "search_query")
    for article in articles:
        article["source_id"] = article.get("source", {}).get("id")
        article["source_name"] = article.get("source", {}).get("name")
        article["publish_date"] = article.get("publishedAt")
        article["insert_date"] = datetime.now().isoformat()
        article["signal_topic"] = query_obj.get("signal_topic")
        article["search_query"] = query_obj.get("query_string")
        cleaned_articles.append({k: article.get(k) for k in target_keys})

    return cleaned_articles
