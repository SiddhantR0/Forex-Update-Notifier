# Importing
import logging
import requests

# Logger instance for mobile notification dispatches
logger = logging.getLogger(__name__)


# Sends push alert to phone using ntfy.sh endpoint
def send_push_notification(
    data_record: dict, topic: str = "siddhant_nrb_gbp_rates"
):
    if not data_record:
        return

    endpoint_url = f"https://ntfy.sh/{topic}"

    curr = data_record["currency"]
    buy = data_record["buy_per_unit"]
    sell = data_record["sell_per_unit"]
    date = data_record["record_date"]

    message = (
        f"📅 Date: {date}\n"
        f"💷 1 {curr} Buying  : NPR {buy}\n"
        f"💷 1 {curr} Selling : NPR {sell}"
    )

    headers = {
        "Title": f"Daily Forex Rate: {curr} to NPR",
        "Priority": "default",
        "Tags": "chart_with_upwards_trend,moneybag",
    }

    try:
        response = requests.post(
            endpoint_url,
            data=message.encode("utf-8"),
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        logger.info(
            f"[Alert Dispatcher] Push notification sent to ntfy channel '{topic}'."
        )
    except Exception as error:
        logger.error(f"[Alert Dispatcher] Failed to deliver push alert: {error}")