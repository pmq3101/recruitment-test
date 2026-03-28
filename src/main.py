import argparse
import logging
import time
import os
from datetime import datetime

from memory_utils import get_peak_memory_mb
from parser import stream_csv
from aggregator import aggregate_campaigns, compute_metrics, top_n_by_ctr, top_n_by_cpa
from writer import write_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Logs directory (relative to script location)
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")


def write_benchmark_log(timings: dict, input_path: str, total_campaigns: int, stats: tuple, peak_memory_mb: float):
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOGS_DIR, f"benchmark_{timestamp}.log")

    file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
    success_count, skip_count = stats

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== Benchmark Log ===\n")
        f.write(f"Timestamp       : {datetime.now().isoformat()}\n")
        f.write(f"Input file      : {input_path}\n")
        f.write(f"File size       : {file_size_mb:.2f} MB\n")
        f.write(f"Total campaigns : {total_campaigns}\n")
        f.write(f"Processed rows  : {success_count}\n")
        f.write(f"Skipped rows    : {skip_count}\n")
        f.write(f"Peak memory     : {peak_memory_mb:.2f} MB\n")
        f.write(f"\n--- Timing Breakdown ---\n")
        for step, elapsed in timings.items():
            f.write(f"{step:30s}: {elapsed:.4f}s\n")
        f.write(f"{'TOTAL':30s}: {sum(timings.values()):.4f}s\n")

    logger.info(f"Benchmark log saved to: {log_file}")


def main():
    arg_parser = argparse.ArgumentParser(
        description="Ad Performance Aggregator — Aggregate CSV ad data by campaign."
    )
    arg_parser.add_argument(
        "--input", required=True, help="Path to input CSV file (ad_data.csv)"
    )
    arg_parser.add_argument(
        "--output", required=True, help="Output directory for result CSV files"
    )
    args = arg_parser.parse_args()

    input_path = args.input
    output_dir = args.output

    if not os.path.isfile(input_path):
        logger.error(f"Input file not found: {input_path}")
        return 1

    logger.info(f"Processing: {input_path}")
    timings = {}

    try:
        # --- Step 1: Stream & Aggregate ---
        logger.info("Step 1: Streaming and aggregating data...")
        t1 = time.time()
        rows = stream_csv(input_path)
        campaigns_raw, stats = aggregate_campaigns(rows)
        timings["Stream & Aggregate"] = time.time() - t1

        success_count, skip_count = stats
        logger.info(
            f"  -> {timings['Stream & Aggregate']:.4f}s (Success: {success_count}, Skipped: {skip_count})"
        )

        if not campaigns_raw:
            logger.warning("No valid campaign data found. Exiting.")
            return 0

        # --- Step 2: Compute metrics ---
        logger.info("Step 2: Computing CTR and CPA...")
        t2 = time.time()
        campaigns = compute_metrics(campaigns_raw)
        timings["Compute Metrics"] = time.time() - t2
        logger.info(f"  -> {timings['Compute Metrics']:.4f}s")

        # --- Step 3: Rank & Output ---
        logger.info("Step 3: Ranking and writing output files...")
        t3 = time.time()
        top_ctr = top_n_by_ctr(campaigns)
        top_cpa = top_n_by_cpa(campaigns)

        ctr_path = os.path.join(output_dir, "top10_ctr.csv")
        cpa_path = os.path.join(output_dir, "top10_cpa.csv")

        write_csv(top_ctr, ctr_path)
        write_csv(top_cpa, cpa_path)
        timings["Rank & Write Output"] = time.time() - t3
        logger.info(f"  -> {timings['Rank & Write Output']:.4f}s")

        # --- Summary ---
        peak_memory_mb = get_peak_memory_mb()
        
        total_time = sum(timings.values())
        logger.info(f"Done! Total campaigns: {len(campaigns)}")
        logger.info(f"Output: {ctr_path}, {cpa_path}")
        logger.info(f"Total processing time: {total_time:.2f}s")
        logger.info(f"Peak memory usage: {peak_memory_mb:.2f} MB")

        # --- Write benchmark log ---
        write_benchmark_log(timings, input_path, len(campaigns), stats, peak_memory_mb)
    except UnicodeDecodeError:
        logger.error(f"Cannot decode input file as UTF-8: {input_path}")
        return 1
    except OSError as e:
        logger.error(f"I/O error while processing output in '{output_dir}': {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
