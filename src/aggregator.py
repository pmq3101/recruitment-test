from collections import defaultdict
from typing import Dict, List, Generator, Tuple


def aggregate_campaigns(rows: Generator[Dict, None, Tuple[int, int]]) -> Tuple[Dict[str, Dict], Tuple[int, int]]:
    """
    Aggregate data from streamed rows by campaign_id.
    Returns:
        tuple containing:
            - Dict[campaign_id, {total_impressions, total_clicks, total_spend, total_conversions}]
            - Tuple[successful_count, skipped_count] from the generator return value
    """
    campaigns = defaultdict(lambda: {
        "total_impressions": 0,
        "total_clicks": 0,
        "total_spend": 0.0,
        "total_conversions": 0,
    })

    rows_iter = iter(rows)
    stats = (0, 0)
    while True:
        try:
            row = next(rows_iter)
            cid = row["campaign_id"]
            campaigns[cid]["total_impressions"] += row["impressions"]
            campaigns[cid]["total_clicks"] += row["clicks"]
            campaigns[cid]["total_spend"] += row["spend"]
            campaigns[cid]["total_conversions"] += row["conversions"]
        except StopIteration as e:
            # e.value contains the (success_count, skip_count) from stream_csv
            if e.value:
                stats = e.value
            break

    return dict(campaigns), stats


def compute_metrics(campaigns: Dict[str, Dict]) -> List[Dict]:
    """
    Compute CTR and CPA for each campaign.
    Returns:
        List of dicts with all metrics for each campaign.
    """
    results = []
    for cid, data in campaigns.items():
        total_impressions = data["total_impressions"]
        total_clicks = data["total_clicks"]
        total_spend = data["total_spend"]
        total_conversions = data["total_conversions"]

        ctr = total_clicks / total_impressions if total_impressions > 0 else 0.0
        cpa = total_spend / total_conversions if total_conversions > 0 else None

        results.append({
            "campaign_id": cid,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_spend": total_spend,
            "total_conversions": total_conversions,
            "CTR": ctr,
            "CPA": cpa,
        })

    return results


def top_n_by_ctr(campaigns: List[Dict], n: int = 10) -> List[Dict]:
    sorted_list = sorted(campaigns, key=lambda x: x["CTR"], reverse=True)
    return sorted_list[:n]


def top_n_by_cpa(campaigns: List[Dict], n: int = 10) -> List[Dict]:
    valid = [c for c in campaigns if c["CPA"] is not None]
    sorted_list = sorted(valid, key=lambda x: x["CPA"])
    return sorted_list[:n]
