import os
from dotenv import load_dotenv
# from ingestion.utils.bq_client import insert_rows
from headline_scraper import run_headline_scraper


load_dotenv()


def main():
    run_headline_scraper()


if __name__ == "__main__":
    main()
