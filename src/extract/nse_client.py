from datetime import datetime
import pandas_market_calendars as mcal

from pyrate_limiter import Rate, Limiter
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import httpx
from config.config import client_config

# Rate limiting
limiter = Limiter(
    Rate(
        client_config.rate_limit.max_requests,
        client_config.rate_limit.duration_milliseconds
    )
)

# Retry decorator
retry_download_bhavcopy = retry(
    stop=stop_after_attempt(client_config.retry.stop_after_attempts),
    wait=wait_exponential(
        multiplier=client_config.retry.wait_multiplier,
        min=client_config.retry.wait_min,
        max=client_config.retry.wait_max),
    retry=retry_if_exception_type((httpx.TransportError, httpx.HTTPStatusError))
)

class NSEClient:
    def __init__(self):
        self.archive_url = client_config.archive_url
        self.headers = client_config.headers.model_dump(by_alias=True)

        self._client = httpx.Client(
            headers = self.headers,
            timeout = client_config.connection_timeout
        )

        self._download_dir = client_config.download_dir

        self._nse_calendar = mcal.get_calendar('NSE')

    @retry_download_bhavcopy
    def download_bhavcopy(self, date: datetime):
        date_str = date.strftime("%Y%m%d")

        # Check for trading holiday
        valid_days = self._nse_calendar.valid_days(date_str, date_str)
        if valid_days.empty:
            raise RuntimeError(f"{date_str} is a trading holiday")

        url = f"{self.archive_url}/content/fo/BhavCopy_NSE_FO_0_0_0_{date_str}_F_0000.csv.zip"

        limiter.try_acquire('bhavcopy_api') # Request rate limit
        r = self._client.get(url, headers=self.headers)
        print(r.url, r.status_code)

        r.raise_for_status()

        if r.headers.get('content-type') and "text/html" in r.headers.get('content-type'):
            raise RuntimeError("NSE file is unavailable or not yet updated.")

        print(r.headers.get('content-type'))

        file_name = url.split("/")[-1]
        file_path = self._download_dir / file_name
        file_path.write_bytes(r.content)
        print(f"Saved to {file_path}")

    def close(self):
        self._client.close()
