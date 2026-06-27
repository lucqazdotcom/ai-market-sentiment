import requests
from dotenv import load_dotenv
import os

from constants.companies import COMPANIES
from constants.news_keywords import TRUSTED_DOMAINS, ROLE_ANCHORS, SIGNAL_TOPICS
from ingestion.utils.bq_client import write_to_big_query

load_dotenv()

query_params = {
    "apiKey": os.getenv("NEWSAPI_KEY"),
    "from": "2026-06-01",
    "domains": TRUSTED_DOMAINS,
    "languages": "en",
    "sortBy": "popularity",
    "searchIn": "title,description"
}


def run_headline_scraper():
    BASE_URL = "https://newsapi.org/v2/everything?"
    print(TRUSTED_DOMAINS)

    # query_group = build_query()
    #
    # for query_obj in query_group:
    #     data = get_articles(BASE_URL, query_obj)
    #     write_to_big_query(data, "raw", "headlines")


def build_query() -> list:
    query_groups = []

    for group, targets in SIGNAL_TOPICS.items():
        phrases = " OR ".join(targets["phrases"])

        if targets["role_anchor_group"]:
            roles = " OR ".join(ROLE_ANCHORS[targets["role_anchor_group"]])
            query_groups.append({
                "signal_topic": group,
                "role_anchor_group": targets.get("role_anchor_group"),
                "query_string": f"({phrases}) AND ({roles})"
            })

        query_groups.append({
            "signal_topic": group,
            "role_anchor_group": targets.get("role_anchor_group"),
            "query_string": f"({phrases})"
        })

    return query_groups


def get_articles(url: str, query_obj: object) -> object:
    params = {**query_params, "q": query_obj.get("query_string")}
    response = requests.get(url, params=params).json()
    articles = response.get("articles")
    cleaned_articles = []
    target_keys = ("source_id", "source_name", "author", "title",
                   "description", "url", "publish_date", "content",
                   "signal_topic", "role_anchor_group", "search_query")
    for article in articles:
        article["source_id"] = article.get("source", {}).get("id")
        article["source_name"] = article.get("source", {}).get("name")
        article["publish_date"] = article.get("publishedAt")
        article["signal_topic"] = query_obj.get("signal_topic")
        article["role_anchor_group"] = query_obj.get("role_anchor_group")
        article["search_query"] = query_obj.get("query_string")
        cleaned_articles.append({k: article.get(k) for k in target_keys})

    return cleaned_articles
