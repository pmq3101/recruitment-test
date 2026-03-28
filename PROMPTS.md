### Prompt 1
tôi có 1 repository bao gồm 1 file .csv có dung lượng lớn và file readme.md kèm theo nó. tôi muốn bạn đọc và xác nhận cho tôi ý hiểu của tôi xem đúng không
file csv: recruitment\fv-sec-001-software-engineer-challenge\ad_data.csv
readme: recruitment\fv-sec-001-software-engineer-challenge\README.md

### Prompt 2
tôi đang hiểu phần yêu cầu này là mình sẽ tạo 1 đoạn code, đọc file, sau đó xuất ra 2 file dữ liệu như theo yêu cầu
phần chính ở đây là tối ưu tốc độ xử lý
để làm được cái này thì tránh việc load cả file vào ram

### Prompt 3
hãy phân tích file csv:
các cột dữ liệu và ý nghĩa
các vấn đề có thể gặp khi xử lý (null, malformed, encoding, duplicate)

### Prompt 4
hãy phân tích chi tiết yêu cầu từ README.md:
input gồm những gì
output cần tạo ra là gì 
business logic cần xử lý
các edge case có thể xảy ra như là: file lỗi, thiếu data, duplicate, ...
constraint về performance (nếu có)

### Prompt 5
ok, vậy các cách tiếp cận có thể có để xử lý
tôi đang nghĩ đến cách sử dụng stream

### Prompt 6
hãy đề xuất nhiều approach khác nhau:
với mỗi approach:
ưu và nhược điểm
memory usage
performance
và đề xuất approach phù hợp nhất cho bài này

### Prompt 7
so sánh stream và buffered stream

### Prompt 8
trước khi bắt đầu code, hãy thiết kế:
flow xử lý dữ liệu từ input -> output
chia module (reader, processor, writer)
trách nhiệm từng module
cách các module giao tiếp với nhau
đảm bảo code dễ test và maintain

### Prompt 9
ok, trước khi bắt đầu, bạn hãy tạo các file markdown lưu lại các yêu cầu vào thư mục test để có thể dễ năm bắt trong quá trình làm việc
hãy chia ra theo nhóm yêu cầu
ví dụ:
yêu cầu về hiệu năng
yêu cầu về cấu trúc code

### Prompt 10
về code quality, tôi muốn thêm là các phần code được tổ chức ở các file riêng biệt về chức năng, không viết vào cùng 1 file main duy nhất.
hãy định nghĩa:
coding convention (naming, structure)
error handling strategy
logging format
config management (nếu có)

### Prompt 11
ok, ta sẽ bắt đầu code ở thư mục test.
tôi muốn sử dụng python để bắt đầu, hãy tạo các phần file trước cho tôi sử dụng kỹ thuật buffered stream, tôi sẽ kiểm tra.
trước khi implement logic chi tiết, hãy:
tạo project structure hoàn chỉnh và tạo khung cho các class
hãy nhớ bổ sung các việc:
xử lý lỗi khi đọc file (file không tồn tại, encoding lỗi)
xử lý dòng dữ liệu lỗi (skip/log)
đảm bảo chương trình không crash khi gặp lỗi

### Prompt 12
tạo 1 thư mục chứa file các file log ghi kết quả các lần test.
hãy thiết kế logging:
log format (timestamp, level, message)
phân loại log (info, error, performance)
log ra file riêng cho từng lần chạy

### Prompt 13
bổ sung logic tính thời gian chạy chương trình.

### Prompt 14
tạo các unit test để chạy thử chương trình.
hãy thiết kế test:
test với file nhỏ
test với file lớn giả lập
test dữ liệu lỗi
test performance cơ bản

### Prompt 15
ok tạo file readme.md để hướng dẫn người dùng sử dụng, trong đó có:
cách chạy
cấu trúc project
giải thích approach (tại sao dùng streaming)

### Prompt 16
tạo file prompts.md lưu lại các prompt đã dùng

### Prompt 17
ok, cuối cùng bạn hãy kiểm tra lại logic code:
1. xem đã hoàn thiện đầy đủ yêu cầu chức năng chưa
2. việc xử lý các edge case được đề cập đã có chưa
tiếp sau đó về unit test, test suit đã bao gồm đầy đủ việc test chức năng, test các error chưa

### Prompt 18
ok, tôi thấy bạn chưa có unit test cho case file không có data và chưa đếm số dòng thành công hay bỏ qua


### Prompt 19
tổng kết lại những gì đã làm được

### Prompt 20
tôi muốn lập tài liệu về các edge case của bài toán này

### Prompt 21
tôi muốn tạo ra 1 file để so sánh tốc độ chạy của stream và buffered stream

### Prompt 22
tôi muốn update lại readme, phần chạy với docker, vì chạy qua docker có thể ảnh hưởng đến performance

### Prompt 23
hãy update thêm logic tính toán Peak memory usage

### Prompt 24
chạy khoảng 10 lần và cho ra con số peak memory vào trong readme nhé