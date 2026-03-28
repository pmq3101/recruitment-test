# Yêu cầu hiệu năng (Performance Requirements)

## Vấn đề cốt lõi
File input ~1GB → **KHÔNG được load toàn bộ vào RAM**.

## Chiến lược xử lý

### ✅ Stream (Line-by-line / Buffered)
- Đọc từng dòng hoặc từng buffer
- Parse → cộng dồn vào `HashMap<campaign_id, Metrics>`
- Bỏ dòng sau khi xử lý → RAM luôn ở mức thấp

### Kỳ vọng hiệu năng
| Metric | Mục tiêu |
|---|---|
| Peak memory | Vài MB (không phụ thuộc kích thước file) |
| Thời gian xử lý | ~10-30s cho file 1GB |
| I/O strategy | Buffered streaming |

## Các điểm tối ưu cần lưu ý

1. **Buffer size**: Sử dụng buffer đủ lớn (8KB–64KB) để giảm số lần đọc I/O
2. **Tránh tạo object thừa**: Parse trực tiếp, tránh tạo intermediate objects không cần thiết
3. **HashMap pre-sizing**: Nếu biết trước số campaign (~50), pre-allocate HashMap
4. **String interning**: Tái sử dụng campaign_id string thay vì tạo mới mỗi dòng

## Đo lường (cần báo cáo trong README)
- [ ] Thời gian xử lý tổng
- [ ] Peak memory usage
- [ ] (Optional) Benchmark logs
