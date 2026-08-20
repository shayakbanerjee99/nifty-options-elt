from datetime import datetime
import pandas_market_calendars as mcal

import httpx
from pyrate_limiter import Rate, Limiter
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.config import client_config

import logging
logger = logging.getLogger(__name__)

"""HTTP client for downloading NSE F&O bhavcopy files, with NSE-calendar-aware
holiday checking, rate limiting, and retry on transient failures."""

# Rate limiting - Same instance is shared across all NSEClient instances
limiter = Limiter(
    Rate(
        client_config.rate_limit.max_requests,
        client_config.rate_limit.duration_milliseconds
    )
)

# Retry decorator - Retries on network/HTTP errors
retry_download_bhavcopy = retry(
    stop=stop_after_attempt(client_config.retry.stop_after_attempts),
    wait=wait_exponential(
        multiplier=client_config.retry.wait_multiplier,
        min=client_config.retry.wait_min,
        max=client_config.retry.wait_max),
    retry=retry_if_exception_type((httpx.TransportError, httpx.HTTPStatusError))
)

class NSEClient:
    """Wrapper around httpx.Client for fetching NSE bhavcopy zip files."""

    def __init__(self):
        self.archive_url = client_config.archive_url
        self.headers = client_config.headers.model_dump(by_alias=True)

        self._client = httpx.Client(
            headers = self.headers,
            timeout = client_config.connection_timeout
        )

        self._download_dir = client_config.download_dir
        self._nse_calendar = mcal.get_calendar('NSE')

        logger.debug("NSEClient initialized with download_dir=%s", self._download_dir)

    @retry_download_bhavcopy
    def download_bhavcopy(self, date: datetime)->str :
        """Downloads the bhavcopy zip for the given date and saves it to disk.

        Raises RuntimeError if the date is a trading holiday, or if NSE returns
        an HTML page instead of the file (happens when the file isn't published yet).
        Returns the path the zip was saved to.
        """
        date_str = date.strftime("%Y%m%d")

        # Check for trading holiday
        valid_days = self._nse_calendar.valid_days(date_str, date_str)
        if valid_days.empty:
            raise RuntimeError(f"{date_str} is a trading holiday")

        url = f"{self.archive_url}/content/fo/BhavCopy_NSE_FO_0_0_0_{date_str}_F_0000.csv.zip"

        limiter.try_acquire('bhavcopy_api') # Request rate limit
        logger.info("Requesting bhavcopy for %s", date_str)

        r = self._client.get(url, headers=self.headers)

        r.raise_for_status()

        # NSE returns a 200 with an HTML error page (not a proper 404) when the
        # file for the given date isn't published. Check content-type to catch this
        if r.headers.get('content-type') and "text/html" in r.headers.get('content-type'):
            logger.warning("NSE returned HTML instead of a file for %s — likely not yet published", date_str)
            raise RuntimeError("NSE file is unavailable or not yet updated.")

        logger.info('content-type: %s', {r.headers.get('content-type')})

        file_name = url.split("/")[-1]
        file_path = self._download_dir / file_name
        file_path.write_bytes(r.content)
        logger.debug(f'Saved to {file_path}')

        return file_path

    def close(self):
        """Closes the underlying httpx client. Call once done downloading."""
        self._client.close()
        logger.debug("NSEClient closed")
