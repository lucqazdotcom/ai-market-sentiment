import os
from dotenv import load_dotenv
from ingestion.utils.bq_client import insert_rows


load_dotenv()


def main():
    rows = [
            {
                "title": "test headline",
                "value": "hello world"
                }
            ]

    insert_rows("raw", "test", rows)


if __name__ == "__main__":
    main()
