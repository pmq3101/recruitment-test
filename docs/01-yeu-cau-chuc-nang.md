# Yêu cầu chức năng (Functional Requirements)

## Mục tiêu
Xây dựng **CLI application** xử lý file CSV quảng cáo và xuất kết quả phân tích.

## Input
- File `ad_data.csv` (~1GB)
- 6 cột: `campaign_id`, `date`, `impressions`, `clicks`, `spend`, `conversions`

## Xử lý — Aggregate theo `campaign_id`

Với mỗi `campaign_id`, tính:

| Metric | Công thức |
|---|---|
| `total_impressions` | SUM(impressions) |
| `total_clicks` | SUM(clicks) |
| `total_spend` | SUM(spend) |
| `total_conversions` | SUM(conversions) |
| `CTR` | total_clicks / total_impressions |
| `CPA` | total_spend / total_conversions |

> [!IMPORTANT]
> Nếu `total_conversions = 0` → CPA = `null` (bỏ qua, không tính)

## Output — 2 file CSV

### `top10_ctr.csv`
- Top 10 campaign có **CTR cao nhất**
- Cột: `campaign_id, total_impressions, total_clicks, total_spend, total_conversions, CTR, CPA`

### `top10_cpa.csv`
- Top 10 campaign có **CPA thấp nhất**
- **Loại bỏ** campaign có `conversions = 0`
- Cột: giống `top10_ctr.csv`

## CLI Interface
```bash
python aggregator.py --input ad_data.csv --output results/
```
