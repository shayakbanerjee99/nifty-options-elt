from nse_client import NSEClient
from datetime import datetime


if __name__ == "__main__":
    client = NSEClient()

    client.download_bhavcopy(datetime.strptime("2026-08-13", "%Y-%m-%d"))
    client.download_bhavcopy(datetime.strptime("2026-08-14", "%Y-%m-%d"))

    client.close()
