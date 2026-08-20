from nse_client import NSEClient

from datetime import datetime
import zipfile

from config.config import extractor_config

import logging
logger = logging.getLogger(__name__)

def extract(zip_file: str, date: datetime):
    with zipfile.ZipFile(zip_file) as zf:
        namelist = zf.namelist()
        csv_path = namelist[0]
        zf.extract(csv_path, extractor_config.extract_dir)

        extracted_csv_path = extractor_config.extract_dir / csv_path
        target_name = f"bhavcopy_{date.strftime('%Y%m%d')}.csv"
        target_path = extractor_config.extract_dir / target_name
        extracted_csv_path.rename(target_path)

        logger.info("Extracted CSV File: %s", target_path)

        return target_path




