from pathlib import Path
from datetime import datetime
from pyrate_limiter import Duration, Rate, Limiter
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import httpx
from tenacity import retry

from config.config import client_config

# Rate limiting
limiter = Limiter(
    Rate(
        client_config.rate_limit.max_requests,
        client_config.rate_limit.duration_milliseconds
    )
)

class NSEClient:
    def __init__(self):
        self.archive_url = client_config.archive_url
        self.headers = client_config.headers.model_dump(by_alias=True)

        self._client = httpx.Client(
            headers = self.headers,
            timeout = 30.0
        )

        self._download_dir = client_config.download_dir

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=3),
        retry=retry_if_exception_type((httpx.TransportError, httpx.HTTPStatusError))
    )
    def download_bhavcopy(self, date: datetime):
        formatted_date = date.strftime("%Y%m%d")
        url = f"{self.archive_url}/content/fo/BhavCopy_NSE_FO_0_0_0_{formatted_date}_F_0000.csv.zip"

        limiter.try_acquire('bhavcopy_api')
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
