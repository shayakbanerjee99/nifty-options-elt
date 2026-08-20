import unittest

from duckdb import DuckDBPyConnection

from db import get_connection
from logging_setup import setup_logging

import logging
logger = logging.getLogger(__name__)

class DBMethods(unittest.TestCase):
    def test_db_connection_successful(self):
        with get_connection() as con:
            self.assertIsNotNone(con)
            self.assertIsInstance(con, DuckDBPyConnection)

            result = con.execute("SELECT 1").fetchone()
            self.assertEqual(result[0], 1)

if __name__ == '__main__':
    setup_logging()
    unittest.main()