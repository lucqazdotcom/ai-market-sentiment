# AI Market Sentiment

An exploratory data pipeline comparing AI displacement narratives in the news with
engineering hiring indicators across the Magnificent Seven companies.

The guiding question:

> Are tracked engineering roles rising, falling, or stable during periods when the
> AI replacement narrative grows?

## How it works

1. Collect news articles through NewsAPI across seven narrative topics.
2. Collect US job-search counts through Adzuna for seven companies and nine role
   search terms.
3. Score article titles and descriptions using VADER.
4. Append observations to BigQuery raw tables.
5. Use dbt to deduplicate observations, calculate weekly metrics, and compare
   narrative and hiring trends.

Tracked companies: Alphabet, Amazon, Apple, Meta, Microsoft, Nvidia, and Tesla.

## Metrics

### Hiring indicator

Job staging retains the latest valid observation for each company, role search,
role group, source, country, and collection date. Currently, valid means the count
is not null.

Daily search counts are summed per company, then averaged within each calendar
week. Weekly outputs include days observed and average search-term coverage.

This measures **tracked search inventory**, rather than unique job openings.
Searches such as “developer” and “software developer” can overlap.

### Narrative indicator

Articles are deduplicated by URL and signal topic, retaining the latest collected
version. An article matching multiple topics retains each association.

Each article/topic receives a directional score:

```text
directional score = topic polarity × absolute VADER compound sentiment
```

| Topic | Polarity |
|---|---:|
| Workforce reduction | +1 |
| AI displacement | +1 |
| Hiring contraction | +1 |
| Junior displacement | +1 |
| Corporate restructuring | +1 |
| Talent demand | −1 |
| AI productivity | 0 |

Positive scores indicate displacement pressure; negative scores indicate
engineering demand. Weekly totals summarize this topic-based narrative indicator.

## Current status

Implemented:

- Both API collectors and explicit BigQuery schemas.
- Append-only raw storage and staging deduplication.
- Title and description sentiment scoring.
- Weekly company hiring averages and narrative aggregates.
- Reporting marts comparing hiring and narrative movement.

All seven dbt models have completed a successful run. That establishes model
execution; data-quality test coverage remains limited.

The current comparison mart aggregates hiring across companies. Per-company
comparisons and rising/falling/stable classifications remain to be completed.

## Setup

### Python environment

The project pins Python 3.13.16 through mise.

From the repository root:

```bash
mise install
mise exec -- python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Alternatively, create the virtual environment using an existing Python 3.13
installation. The requirements file automatically applies `constraints.txt`.

### Environment variables

Create `.env` in the repository root:

```dotenv
GCP_PROJECT_ID=your-project-id
NEWSAPI_KEY=your-newsapi-key
ADZUNA_APP_ID=your-adzuna-app-id
ADZUNA_API_KEY=your-adzuna-api-key
HASH_SIZE=32
```

The collectors load this file automatically. It is excluded from Git.
`HASH_SIZE` must be an integer from 1 to 64 and controls the headline hash length.

### Google Cloud

Install the Google Cloud CLI, enable the BigQuery API, and authenticate:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

Create `raw` and `analytics` datasets in the same location. For US datasets:

```bash
bq --location=US mk --dataset YOUR_PROJECT_ID:raw
bq --location=US mk --dataset YOUR_PROJECT_ID:analytics
```

Skip creation for existing datasets. Your identity needs permission to run BigQuery
jobs and read, create, and write the relevant tables.

The Python loader creates missing raw tables, but does not create datasets.

### dbt connection

Create `~/.dbt/profiles.yml`:

```yaml
ai_market_analysis:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: YOUR_PROJECT_ID
      dataset: analytics
      location: US
      threads: 4
```

Match `location` to your datasets. Update the source project in
`dbt/models/staging/sources.yml` to match your project. The profile, source project,
and `GCP_PROJECT_ID` should point to the intended project. dbt does not load the
Python `.env` file automatically.

Verify the connection from the repository root:

```bash
cd dbt
dbt debug
```

## Run

From the repository root, with the virtual environment activated:

```bash
python src/main.py
```

This runs both collectors and appends observations to BigQuery. Job collection
pauses for 60 seconds after batches of 25 requests.

Then, from the repository root, load the polarity mapping, build the models, and
run their configured tests:

```bash
cd dbt
dbt seed --select signal_topic_polarity
dbt build
```

Reporting outputs:

- `mart_narrative_trend`: weekly net displacement narrative score.
- `mart_market_contradiction`: aggregate hiring and narrative scores with changes
  from the previous available observation.

## Limitations

- Overlapping job searches can count the same opening more than once.
- Adzuna coverage represents one source and the US market.
- Incomplete collection days or weeks can affect comparisons.
- News collection currently fetches one page per topic.
- Topic membership does not establish whether an article supports or disputes
  displacement.
- Sentiment strength measures language tone, rather than evidence strength.
- Articles can contribute to multiple topic scores.
- Comparisons are exploratory and do not establish that AI causes hiring changes.

## Remaining work

- Preserve company detail in the final comparison.
- Define rising/falling/stable thresholds.
- Add uniqueness, completeness, and coverage checks.
- Handle missing weeks and signed narrative-score changes explicitly.
- Improve API error handling, retries, and pagination.
- Correct headline ID construction and reset job-search candidates between runs.
- Add scheduling, monitoring, and a dashboard.
