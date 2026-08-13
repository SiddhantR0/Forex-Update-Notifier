# Importing
import csv
import logging
from pathlib import Path

# Logger instance for file storage operations
logger = logging.getLogger(__name__)


# Writes parsed rates to CSV file with headers and handles deduplication
def save_record_to_csv(
    data_record: dict, file_path: str = "data/forex_history.csv"
):
    if not data_record:
        logger.warning("[Storage Handler] Received empty record. Skipping save.")
        return

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(data_record.keys())
    existing_rows = []
    record_exists = False

    # Check for duplicate entry if storage file already exists
    if path.exists():
        with open(path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (
                    row.get("record_date") == data_record["record_date"]
                    and row.get("currency") == data_record["currency"]
                ):
                    record_exists = True
                    # Replace existing entry for the same date/currency pair
                    existing_rows.append(data_record)
                else:
                    existing_rows.append(row)

        if record_exists:
            logger.info(
                f"[Storage Handler] Record for {data_record['record_date']} exists. Updating entry..."
            )
            with open(path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_rows)
            return

    # Append new record if not already present
    file_exists = path.exists()
    with open(path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_record)

    logger.info(f"[Storage Handler] Record saved successfully to '{file_path}'.")