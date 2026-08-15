from nse_client import NSEClient
from datetime import datetime
from config.logging_setup import setup_logging

if __name__ == "__main__":
    setup_logging()
    client = NSEClient()

    client.download_bhavcopy(datetime.strptime("2026-08-13", "%Y-%m-%d"))
    client.download_bhavcopy(datetime.strptime("2026-08-14", "%Y-%m-%d"))

    client.close()
