import unittest
import zipfile

from httpx import HTTPStatusError

from logging_setup import setup_logging
from nse_client import NSEClient
from datetime import datetime, timedelta
import os

import logging
logger = logging.getLogger(__name__)

class NSEClientMethods(unittest.TestCase):
    def test_download_bhavcopy_successfully(self):
        nse_client = NSEClient()
        try:
            date = datetime(2026, 8, 13)
            zip_path = nse_client.download_bhavcopy(date)

            self.assertTrue(os.path.exists(zip_path))
            self.assertGreater(os.path.getsize(zip_path), 0)
            self.assertTrue(zipfile.is_zipfile(zip_path))

            with zipfile.ZipFile(zip_path) as zf:
                self.assertTrue(len(zf.namelist()) > 0)

        except RuntimeError as e:
            logger.error(e)
            self.fail(f"download_bhavcopy raised RuntimeError: {e}")
        finally:
            nse_client.close()

    def test_download_bhavcopy_on_trading_holiday(self):
        nse_client = NSEClient()
        try:
            date = datetime(2026, 8, 16)
            nse_client.download_bhavcopy(date)
        except RuntimeError as e:
            logger.error(e)
            self.assertTrue(f"download_bhavcopy raised RuntimeError: {e}")
            self.assertEqual(e.args[0], "20260816 is a trading holiday")

        finally:
            nse_client.close()


if __name__ == '__main__':
    setup_logging()
    unittest.main()