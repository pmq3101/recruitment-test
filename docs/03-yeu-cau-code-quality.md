# Yêu cầu chất lượng code (Code Quality Requirements)

## Tổ chức code (Separation of Concerns)
- **Tách code theo chức năng vào các file riêng biệt**, KHÔNG viết tất cả vào 1 file main duy nhất
- Mỗi file/module chịu trách nhiệm 1 chức năng cụ thể:
  - Parsing CSV → file riêng
  - Logic aggregate → file riêng
  - Ghi output CSV → file riêng
  - Entry point CLI → file riêng (chỉ gọi các module khác)

## Clean Code
- Đặt tên biến/hàm có ý nghĩa rõ ràng
- Consistent coding style
- Không có dead code hoặc code bị comment-out
- Cấu trúc rõ ràng, tách biệt trách nhiệm

## Error Handling
- File không tồn tại → thông báo lỗi rõ ràng
- Dòng CSV bị lỗi (malformed rows) → skip + log warning
- Edge cases: file rỗng, header sai format, giá trị âm, v.v.

## Testing
- Unit test kiểm tra tính đúng đắn kết quả aggregate
- Test edge cases: `conversions = 0`, dòng lỗi, file rỗng
- Test tính toán CTR, CPA ....

## Cấu trúc project gợi ý
```
project/
├── src/               # Source code chính
│   ├── main.*         # Entry point (CLI)
│   ├── parser.*       # CSV parsing logic
│   ├── aggregator.*   # Aggregate logic
│   └── writer.*       # Output CSV writer
├── tests/             # Unit tests
├── results/           # Output files
│   ├── top10_ctr.csv
│   └── top10_cpa.csv
├── README.md
├── Dockerfile         # (Optional)
└── PROMPTS.md         # (Nếu dùng AI)
```
