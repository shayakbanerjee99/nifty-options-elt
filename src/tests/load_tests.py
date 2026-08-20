import os
import unittest

from db import get_connection
from load import load_bhavcopy
from logging_setup import setup_logging

import logging

from schema import create_schema

logger = logging.getLogger(__name__)

class LoadMethods(unittest.TestCase):
    TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')

    def test_loading_is_successful(self):
        with get_connection() as con:
            csv_file_path = os.path.join(self.TEST_DATA_DIR, 'test_bhavcopy_20260813.csv')
            self.assertTrue(os.path.exists(csv_file_path), f"File not found at {csv_file_path}")

            create_schema(con)
            load_bhavcopy(con, csv_file_path, 'NIFTY')

            result = con.execute(
                "SELECT * FROM nifty_options WHERE symbol = 'NIFTY' ORDER BY expiry_date"
            ).fetchall()

            self.assertTrue(len(result) > 0, "No rows returned for NIFTY")

if __name__ == '__main__':
    setup_logging()
    unittest.main()