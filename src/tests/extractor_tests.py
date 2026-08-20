import csv
import unittest

from extractor import extract
from logging_setup import setup_logging
from nse_client import NSEClient
from datetime import datetime
import os

import logging
logger = logging.getLogger(__name__)

class ExtractorMethods(unittest.TestCase):
    def test_extract_successful(self):
        nse_client = NSEClient()
        zip_path = None
        csv_file_path = None
        try:
            date = datetime(2026, 8, 14)
            zip_path = nse_client.download_bhavcopy(date)
            csv_file_path = extract(zip_path, date)

            self.assertTrue(os.path.exists(csv_file_path))
            self.assertTrue(str(csv_file_path).endswith('.csv'))
            self.assertGreater(os.path.getsize(csv_file_path), 0)

            with open(csv_file_path, newline='') as f:
                reader = csv.reader(f)
                header = next(reader)
                self.assertGreater(len(header), 0)
        finally:
            for p in (zip_path, csv_file_path):
                if p and os.path.exists(p):
                    os.remove(p)
            nse_client.close()


if __name__ == '__main__':
    setup_logging()
    unittest.main()