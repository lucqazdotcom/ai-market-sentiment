import os
from dotenv import load_dotenv
# from ingestion.utils.bq_client import insert_rows
from headline_scraper import run_headline_scraper
from job_scrapper import run_job_scrapper


load_dotenv()


def main():
    # run_headline_scraper()
    run_job_scrapper()


if __name__ == "__main__":
    main()
