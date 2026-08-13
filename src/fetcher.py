# Importing
import datetime
import logging
import requests

# Logger instance for fetching raw rates
logger = logging.getLogger(__name__)


# Connects to official NRB API and fetches rates JSON for a specific date
def fetch_nrb_exchange_rates(date_str: str = None) -> dict:
    if not date_str:
        date_str = datetime.date.today().strftime("%Y-%m-%d")

    url = "https://www.nrb.org.np/api/forex/v1/rates"
    params = {"page": 1, "per_page": 1, "from": date_str, "to": date_str}

    logger.info(f"[Data Acquisition] Requesting NRB API payload for: {date_str}")

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        logger.info("[Data Acquisition] Successfully fetched API response.")
        return response.json()
    except requests.exceptions.RequestException as error:
        logger.error(
            f"[Data Acquisition] Network or HTTP error during fetch: {error}"
        )
        raise