# Ad Performance Aggregator — 1GB Dataset Challenge

A high-performance command-line application designed to process large advertising datasets (~1GB+) with minimal memory footprint. This project calculates aggregated metrics (CTR, CPA) per campaign and identifies top performers.

---

## How to Run

### Preparation
Before running the application, make sure you have placed the input CSV file correctly:
1. Create a `data` folder in the root of the project.
2. Unzip and place the downloaded `ad_data.csv` into this `data/` folder.

```bash
mkdir data
# Place ad_data.csv inside the data/ folder
```

### Method 1: Local Python (Recommended)
No external libraries are required. The application uses only Python's standard library.

```bash
# Run the aggregator
python src/main.py --input data/ad_data.csv --output results/
```

### Method 2: Docker
```bash
# Build the image
docker build -t ad-aggregator .

# Run the container (Mounting current directory to /app_data)
docker run --rm -v "${PWD}:/app_data" ad-aggregator --input /app_data/data/ad_data.csv --output /app_data/results/
```

> [!NOTE]
> **Performance Note:** Running Docker on Windows/macOS is slower due to the filesystem bridge (I/O bottleneck via WSL2/Hypervisor on the `-v` mount). Native Linux deployments will not have this overhead and match local performance.

## Project Structure
The project is organized into clear modules following the **Separation of Concerns** principle:

```text
test/
├── src/                # Core Source Code
│   ├── main.py         # Entry point & CLI orchestration
│   ├── parser.py       # Buffered streaming & CSV row validation
│   ├── aggregator.py   # Aggregation logic & ranking
│   └── writer.py       # Formatted CSV output generation
├── tests/              # Unit Tests (Standard unittest framework)
├── docs/               # Detailed requirement analysis & planning
├── logs/               # Automated benchmark and execution logs
├── results/            # Default output directory for aggregated results
├── run_tests.py        # Test runner script
├── Dockerfile          # Container configuration
└── README.md           # Project documentation (this file)
```

## Approach

### The Challenge
Processing a **1GB CSV file** presents a memory risk. Traditional approaches like `pandas.read_csv()` would attempt to load the entire dataset into RAM, which could consume 2-4GB of memory depending on data fragmentation, likely crashing on standard machines or exceeding resource limits.

### Our Solution: Buffered Line-by-Line Streaming
Instead of loading the file, we treat it as a **continuous stream**:
1.  **Buffered Input:** Using Python's `open()` with a built-in buffer (typically 8KB), we read chunks of data from the disk, minimizing expensive System Calls.
2.  **Generator-based Parsing:** We use a Python `generator` to yield one row at a time. As soon as a row is processed and added to the aggregate counts, it is discarded from memory.
3.  **Constant Memory Footprint:** Since we only have ~50 campaigns, we only need to keep 50 small objects in a `HashMap`, so memory usage stays low and scales with campaign cardinality instead of file size.

---

## Performance & Benchmarks

### 1GB Dataset Execution
The application is highly optimized. Testing on a simulated **~1GB dataset** (~26.8 million rows, 50 campaigns) guarantees completion within seconds while using virtually no RAM:
- **Execution Time:** ~53 to 104 seconds (depending on local disk read speeds).
- **Peak Memory Usage:** **~16.83 MB** (Averaged over 10 consecutive runs). Measured with zero-overhead OS-native profiling (`ctypes` on Windows, `resource` on macOS, `/proc` on Linux).

Thanks to the Generator-based design, RAM usage scales purely with the cardinality of unique campaigns, *not* input file size.

### Stream vs Buffered Stream Comparison
To validate the necessity of **Buffered Streaming**, we created `compare_streams.py` to test reading 50,000 lines. The results clearly demonstrate why native Unbuffered I/O is practically unusable for 1GB files:

- **Buffered Stream (Our Approach):** ~0.008 seconds
- **Unbuffered Stream (Byte-by-Byte):** ~7.962 seconds
- **Performance Gain:** **~983x Faster**

By relying on Python's built-in block buffer (`TextIOWrapper` + `BufferedReader`), the CPU requests large chunks (e.g., 8KB) from the OS at a time. Without it, the application becomes bottlenecked by constant I/O System Calls.

---

## Robustness & Edge Cases
The application is designed to be "production-ready" by handling various data quality issues:
-   **Negative Values:** Automatically detects and skips rows with negative impressions, clicks, etc.
-   **Malformed Rows:** Gracefully skips lines with missing columns or invalid data types without crashing.
-   **Division by Zero:** Safely handles cases where impressions or conversions are zero (CTR = 0.0, CPA = None).
-   **Encoding:** Includes error trapping for `UnicodeDecodeError` to handle corrupted file streams.
-   **Statistics:** Generates a detailed report of successful vs. skipped rows at the end of each run.

## Running Tests
We use the standard `unittest` framework. No extra installations are required.
```bash
python run_tests.py
```

## Common Errors

### 1) Missing required CLI arguments
```bash
python src/main.py
```
Expected:
- Error: missing required `--input` and `--output`

### 2) Input file does not exist
```bash
python src/main.py --input does_not_exist.csv --output results/
```
Expected:
- Log: `Input file not found: does_not_exist.csv`

### 3) Invalid output path (points to a file, not a directory)
```bash
python src/main.py --input ad_data.csv --output README.md
```
Expected:
- Log: `I/O error while processing output in 'README.md' ...`
