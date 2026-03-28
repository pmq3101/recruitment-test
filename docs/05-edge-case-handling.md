# Edge Case Handling Documentation

This document outlines the various edge cases, potential data anomalies, and system errors addressed in the Ad Performance Aggregator to ensure robustness and data integrity.

---

## 🛠️ Data Validation & Parsing Errors

| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Malformed Rows** | Rows with missing columns or non-numeric data in numeric fields (e.g., `impressions='abc'`). | **Skip & Log:** Row is skipped. A `WARNING` is logged with the original row content and error message. |
| **Negative Numerical Values** | Negative values for `impressions`, `clicks`, `spend`, or `conversions`. | **Skip & Log:** Ad metrics should not be negative. These rows are skipped to prevent skewing the aggregation. |
| **Whitespace in IDs** | `campaign_id` containing leading/trailing spaces (e.g., `"CMP001 "`). | **Sanitization:** All `campaign_id` strings are `.strip()`ed before aggregation to ensure they group correctly. |
| **Corrupt line endings** | Mixture of `\n` and `\r\n` or trailing empty lines. | **Standardization:** `csv.DictReader` with `newline=""` handles standard CSV line termination variation. |

---

## 📈 Aggregation & Mathematical Errors

| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Zero Impressions** | A campaign has `total_impressions = 0`. Calculating CTR (`clicks / impressions`) would cause a crash. | **Safety Check:** CTR is explicitly set to `0.0` if impressions are 0. |
| **Zero Conversions** | A campaign has `total_conversions = 0`. Calculating CPA (`spend / conversions`) would cause a crash. | **Safety Check:** CPA is set to `None` if conversions are 0. |
| **CPA Ranking Exclusion** | Requirements state to exclude campaigns with zero conversions from the CPA top list. | **Filtering:** The CPA ranking logic filters out any campaign where `CPA is None` before sorting. |
| **Empty Input File** | The input file contains only headers or is completely empty. | **Graceful Exit:** The app detects "0 valid campaigns" and exits with a clear warning instead of crashing or outputting empty files. |

---

## 💻 System & I/O Errors

| Edge Case | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **File Not Found** | The provided `--input` path does not point to a valid file. | **Validation:** Checked before processing. Logs an `ERROR` and stops execution. |
| **Encoding Mismatch** | The CSV is not saved in `UTF-8` (e.g., `Latin-1` or `UTF-16`). | **Error Trapping:** `UnicodeDecodeError` is caught in the streaming loop to provide a descriptive error message. |
| **Output Access Denied** | The application doesn't have permissions to write to the requested `--output` directory. | **Pre-creation:** Uses `os.makedirs(exist_ok=True)` and standard exception handling for file writes. |

---

## 📊 Statistics Reporting
To provide transparency on data quality, every execution generates a summary:
- **Processed Rows:** Number of rows successfully aggregated.
- **Skipped Rows:** Number of rows discarded due to being malformed or having negative values.

These stats are visible in the console and permanently recorded in the `logs/benchmark_*.log` files for auditing.
