"""Runs the end-to-end ETL flow for a single trading day: download the NSE
bhavcopy, extract it, and load NIFTY options rows into duckdb."""

from datetime import datetime
import logging

from db import get_connection
from extractor import extract
from load import load_bhavcopy
from nse_client import NSEClient
from schema import create_schema

from logging_setup import setup_logging
logger = logging.getLogger(__name__)


def run_elt(date: datetime) -> None:
    """Extract a bhavcopy CSV, load it into duckdb, applying the NIFTY options schema."""

    nse_client = NSEClient()
    try:
        # Extract
        zip_path = nse_client.download_bhavcopy(date)
        csv_file_path = extract(zip_path, date)
        nse_client.close()

        # Load and Transform
        with get_connection() as con:
            create_schema(con) # idempotent - safe to call every run
            load_bhavcopy(con, csv_file_path, 'NIFTY')

    except RuntimeError as e:
        # Catches holiday/unavailable-file errors raised by NSEClient
        logger.error(e)

if __name__ == '__main__':
    setup_logging()

    date = datetime(2026, 8, 19)
    run_elt(date)

