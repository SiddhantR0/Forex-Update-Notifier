# Importing
import datetime
import logging

# Logger instance for rate parsing and calculations
logger = logging.getLogger(__name__)


# Filters raw NRB payload for target currency and calculates per-unit/mid rates
def parse_currency_data(raw_data: dict, target_currency: str = "GBP") -> dict:
    logger.info(
        f"[Data Processing] Filtering and parsing payload for target: '{target_currency}'"
    )

    if not raw_data or "data" not in raw_data:
        raise ValueError("Received malformed or empty response payload.")

    payload = raw_data.get("data", {}).get("payload", [])
    if not payload:
        logger.warning(
            "[Data Processing] No currency rate payload found for requested date."
        )
        return None

    day_record = payload[0]
    rate_date = day_record.get("date")
    rates_list = day_record.get("rates", [])

    # Find the target currency record from rates array
    matched_rate = None
    for item in rates_list:
        if item.get("currency", {}).get("iso3") == target_currency:
            matched_rate = item
            break

    if not matched_rate:
        raise ValueError(
            f"Target currency '{target_currency}' not present in NRB records."
        )

    # Cast rate values to appropriate numeric types
    unit = int(matched_rate.get("unit", 1))
    buy_rate = float(matched_rate.get("buy", 0.0))
    sell_rate = float(matched_rate.get("sell", 0.0))

    # Calculate per-unit rates and mid-market spread
    buy_per_unit = round(buy_rate / unit, 4)
    sell_per_unit = round(sell_rate / unit, 4)
    mid_rate = round((buy_per_unit + sell_per_unit) / 2, 4)

    parsed_record = {
        "record_date": rate_date,
        "currency": target_currency,
        "currency_name": matched_rate.get("currency", {}).get("name"),
        "unit": unit,
        "buy_rate": buy_rate,
        "sell_rate": sell_rate,
        "buy_per_unit": buy_per_unit,
        "sell_per_unit": sell_per_unit,
        "mid_rate": mid_rate,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    logger.info(
        f"[Data Processing] Parsed 1 {target_currency} -> Buy: NPR {buy_per_unit} | Sell: NPR {sell_per_unit}"
    )
    return parsed_record