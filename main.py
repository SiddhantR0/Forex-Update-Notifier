# Importing
import logging
from src.fetcher import fetch_nrb_exchange_rates
from src.notifier import send_push_notification
from src.parser import parse_currency_data
from src.storage import save_record_to_csv

# Global logging setup for application runtime
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("main")

# Unique channel topic string for ntfy mobile app
NTFY_TOPIC = "siddhant_nrb_gbp_rates"


# Orchestrates fetch, parse, store, and notify steps
def run_pipeline():
    logger.info("Initializing Daily NRB Currency Rate Tracker...")

    try:
        # Step 1: Data Acquisition
        raw_json = fetch_nrb_exchange_rates()

        # Step 2: Data Processing
        gbp_data = parse_currency_data(raw_json, target_currency="GBP")

        if gbp_data:
            # Step 3: Storage Handling
            save_record_to_csv(gbp_data)

            # Step 4: Alert Dispatch
            send_push_notification(gbp_data, topic=NTFY_TOPIC)

        logger.info("Daily NRB Currency Rate Tracker executed successfully.")

    except Exception as err:
        logger.critical(
            f"Fatal error encountered during execution: {err}", exc_info=True
        )


if __name__ == "__main__":
    run_pipeline()