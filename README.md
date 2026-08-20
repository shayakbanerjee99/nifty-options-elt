# nifty-options-elt

Extracts historical F&O data for NIFTY index using daily bhavcopy data published by the NSE, loads it into a local [DuckDB](https://duckdb.org/) database, and transforms it to query F&O data and historical option chains for backtesting multi-leg option strategies

## Description

NSE publishes a daily bhavcopy (end-of-day report) that contains EOD data for all contracts traded on the NSE, but it's only available as a raw CSV inside a zip file. There's no easy way to query across dates or build a historical view of the options market from it directly.

This project automates:
1. **Extract**: downloading the daily bhavcopy zip for a given trading date from the NSE archives (using httpx with retry and rate limiting, and skipping non-trading days automatically) and unzipping the CSV
2. **Load & Transform**:  Loading the NIFTY options rows and transforming it into a DuckDB table (`nifty_options`).

This gives us a single DuckDB file containing clean, typed and queryable historical F&O data for NIFTY symbol. This data can be queried to view historical option chains or to back-test multi-leg option strategies.

## Setup

Requires Python 3.10+. Install the dependencies:

```bash
pip install -r requirements.txt
```

All configurations live in `src/config/config.yaml` and can be edited without touching code.

## Running the pipeline

`src/pipeline.py` runs the full extract-load-transform flow for a single date via `run_elt(date)`.

Change the date to load data for a different date.

```python
if __name__ == '__main__':
    setup_logging()
    date = datetime(2026, 8, 19)
    run_elt(date)
```

The downloaded data is available in the `db_path` configured in `config.yaml` which is `data/db/nsedata.db` by default.

## Viewing the data

With the [DuckDB CLI](https://duckdb.org/docs/api/cli/overview.html) installed, open the database file directly:

```bash
duckdb data/db/nsedata.db
```

From the DuckDB shell:

```sql
.tables
DESCRIBE nifty_options;
SELECT * FROM nifty_options LIMIT 10;
```
