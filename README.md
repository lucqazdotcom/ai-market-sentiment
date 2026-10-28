# AI market sentiment

Track whether open engineering roles at each Magnificent Seven company are rising,
falling, or stable during periods when the AI replacement narrative grows.

The pipeline collects news through NewsAPI and US job-search counts through Adzuna,
scores headline sentiment with VADER, loads raw records into BigQuery, and uses dbt
to produce weekly summaries.

## Current progress

Implemented:

- Seven tracked companies and nine role search terms across five role groups.
- News searches across seven narrative topics and a curated list of domains.
- Title/description sentiment scoring and divergence calculation.
- Explicit BigQuery schemas and append-based loading with table creation.
- dbt staging, intermediate weekly models, topic polarity seeds, and reporting marts.
- Basic dbt `not_null` checks.

This is a prototype. A successful end-to-end run has not been verified in this
review, and the final mart currently aggregates all companies rather than answering
the per-company question above. There is no dashboard, scheduler, CI configuration,
or Python test suite yet.

## Setup

Run the following commands from the repository root unless specified otherwise.

### 1. Install Python dependencies

The repository pins Python 3.13.16 in `mise.toml`. If you use mise:

```bash
mise install
mise exec -- python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Alternatively, create `venv` using your Python 3.13 installation and run the same
activation and pip commands. `requirements.txt` automatically applies the pins in
`constraints.txt`. Installation of these pins has not been validated in this review.

### 2. Configure API credentials

Create a `.env` file in the repository root:

```dotenv
GCP_PROJECT_ID=your-gcp-project-id
NEWSAPI_KEY=your-newsapi-key
ADZUNA_APP_ID=your-adzuna-app-id
ADZUNA_API_KEY=your-adzuna-api-key
HASH_SIZE=32
```

News collection requires a NewsAPI key; job collection requires an Adzuna app ID
and API key. `HASH_SIZE` is required for headline IDs and must be an integer from
1 to 64. The current hash helper also uses this value as its hash key.

Python loads `.env` automatically. It is ignored by Git; keep credentials out of
commits.

### 3. Configure Google Cloud and BigQuery

Install the Google Cloud CLI, enable the BigQuery API for your project, and set up
Application Default Credentials:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

Your authenticated identity needs permission to create BigQuery jobs and to read,
create, and write the pipeline's tables. For automation, configure an appropriate
service identity instead of relying on an interactive login.

Create a `raw` dataset and an analytics dataset, such as `analytics`, in the same
BigQuery location. For example, using the US multi-region:

```bash
bq --location=US mk --dataset YOUR_PROJECT_ID:raw
bq --location=US mk --dataset YOUR_PROJECT_ID:analytics
```

Skip dataset creation if they already exist. The loader creates missing raw tables
using the schemas in `src/ingestion/schema/schema.py`; it does not create datasets.

### 4. Configure dbt

Create `~/.dbt/profiles.yml` with the profile name expected by `dbt/dbt_project.yml`:

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

Use the location of your datasets. In `dbt/models/staging/sources.yml`, replace the
hardcoded `database: ai-sentiment-analysis-498901` with your project ID. This source
setting, the dbt profile project, and `GCP_PROJECT_ID` must point to the intended
project. dbt does not automatically load the Python `.env` file.

Check connectivity:

```bash
cd dbt
dbt debug
cd ..
```

## Run the pipeline

The current entry point runs **job collection only**:

```bash
python src/main.py
```

To run headline collection separately from the repository root:

```bash
PYTHONPATH=src python -c 'from headline_scraper import run_headline_scraper; run_headline_scraper()'
```

Both commands call external APIs and append records to BigQuery. Job collection
pauses for 60 seconds after each batch of 25 searches. Repeated collection runs can
produce duplicate or overlapping data; see the known issues below.

After both raw tables contain data, load the topic polarity seed and build/test the
models:

```bash
cd dbt
dbt seed
dbt build
```

`dbt build` is currently blocked by the job date-column mismatch described below.
The reporting models are `mart_narrative_trend` and `mart_market_contradiction`.

## Known issues and remaining work

### Collection and transformation bugs

- **Job results are dropped:** only batches of 25 are written. Of 63 configured
  searches, the final 13 results are never saved.
- **Job date mismatch:** `int_company_postings_weekly` references `date`, but the
  collector and raw schema use `date_posted`.
- **Repeated initialization duplicates searches:** the global job-search list is
  appended to without being reset.
- **Headline IDs use an unassigned date:** the hash is calculated before
  `publishedAt` is mapped to `publish_date`.
- API calls lack timeouts, status validation, and retries. News collection fetches
  only one page per topic.
- The entry point does not run both collectors or invoke dbt.

### Measurement and reporting gaps

- Weekly job inventory sums repeated snapshots and overlapping search counts.
  Collection frequency can therefore change reported totals without an underlying
  increase in open jobs.
- Headline collection repeatedly appends an overlapping 30-day window without
  deduplication.
- Topic polarity multiplied by absolute sentiment strength does not establish
  whether an article supports or disputes an AI replacement claim.
- The final comparison combines companies. Per-company comparisons,
  rising/falling/stable thresholds, and missing-week handling remain to be defined.
- The comparison mart's tests are commented out; Python tests are absent.

Prioritize collection fixes and a verified end-to-end build, then settle the
measurement definitions before adding scheduling, monitoring, and a dashboard.

## Repository layout

```text
src/
  main.py                  Entry point (currently jobs only)
  headline_scraper.py       NewsAPI collection and sentiment enrichment
  job_scrapper.py           Adzuna job-count snapshots
  sentiment_analysis.py     VADER scoring
  constants/                Companies, roles, topics, and news domains
  ingestion/                BigQuery schemas and loading
dbt/
  seeds/                    Topic polarity mapping
  models/staging/           Raw source wrappers
  models/intermediate/      Headline signals and weekly aggregates
  models/marts/             Narrative and market comparison outputs
tests/                      Placeholder; no Python tests yet
```
