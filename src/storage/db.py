from contextlib import contextmanager
import duckdb
from pathlib import Path
from config.config import db_config

import logging
logger = logging.getLogger(__name__)

@contextmanager
def get_connection(db_path: str = db_config.db_path):

    # Create path if it does not exist
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)
    logger.info(f"DB Connection established to {db_path}")

    try:
        yield con
    finally:
        con.close()
        logger.info("DB Connection closed")