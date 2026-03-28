import csv
import logging
from typing import Generator, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def parse_row(row: Dict[str, str]) -> Optional[Dict]:
    """
    Parse and validate a single CSV row.
    Ensures numerical values are non-negative.
    Returns parsed dict or None if the row is malformed or has negative values.
    """
    try:
        data = {
            "campaign_id": row["campaign_id"].strip(),
            "impressions": int(row["impressions"]),
            "clicks": int(row["clicks"]),
            "spend": float(row["spend"]),
            "conversions": int(row["conversions"]),
        }
        
        # Validate non-negative values
        if any(v < 0 for v in [data["impressions"], data["clicks"], data["spend"], data["conversions"]]):
            logger.warning(f"Skipping row with negative values: {row}")
            return None
            
        return data
    except (KeyError, ValueError) as e:
        logger.warning(f"Skipping malformed row: {row} — Error: {e}")
        return None


def stream_csv(filepath: str) -> Generator[Dict, None, Tuple[int, int]]:
    """
    Stream CSV file line by line.
    Yields each successfully parsed row.
    Returns a tuple of (successful_count, skipped_count) when finished.
    """
    success_count = 0
    skip_count = 0
    
    try:
        with open(filepath, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            try:
                for row in reader:
                    parsed = parse_row(row)
                    if parsed is not None:
                        success_count += 1
                        yield parsed
                    else:
                        skip_count += 1
            except UnicodeDecodeError as e:
                logger.error(f"Encoding error in file {filepath}: {e}")
                raise
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {e}")
        raise
        
    return success_count, skip_count
