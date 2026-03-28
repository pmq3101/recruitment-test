import csv
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

OUTPUT_COLUMNS = [
    "campaign_id",
    "total_impressions",
    "total_clicks",
    "total_spend",
    "total_conversions",
    "CTR",
    "CPA",
]


def format_row(campaign: Dict) -> Dict:
    """
    Format values for output CSV.
    CTR: 4 decimal places
    CPA: 2 decimal places (empty string if None)
    """
    return {
        "campaign_id": campaign["campaign_id"],
        "total_impressions": campaign["total_impressions"],
        "total_clicks": campaign["total_clicks"],
        "total_spend": f'{campaign["total_spend"]:.2f}',
        "total_conversions": campaign["total_conversions"],
        "CTR": f'{campaign["CTR"]:.4f}',
        "CPA": f'{campaign["CPA"]:.2f}' if campaign["CPA"] is not None else "",
    }


def write_csv(data: List[Dict], filepath: str) -> None:
    """
    Write list of campaigns to a CSV file.
    Automatically creates output directory if it doesn't exist.
    """
    output_dir = os.path.dirname(filepath)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(filepath, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            for campaign in data:
                writer.writerow(format_row(campaign))
    except OSError as e:
        logger.error(f"Failed to write output CSV '{filepath}': {e}")
        raise

    logger.info(f"Written {len(data)} rows to {filepath}")
