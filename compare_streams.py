import time
import os

def test_buffered_stream(filepath, num_lines=50000):
    start = time.time()
    count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            count += 1
            if count >= num_lines:    
                break
    return time.time() - start

def test_unbuffered_stream(filepath, num_lines=50000):
    start = time.time()
    count = 0
    with open(filepath, "rb", buffering=0) as f:
        while count < num_lines:
            line = bytearray()
            while True:
                char = f.read(1)
                if not char:
                    break
                line.extend(char)
                if char == b'\n':
                    break
            if not line:
                break
            count += 1
    return time.time() - start

if __name__ == "__main__":
    candidates = [
        "../recruitment/data/ad_data.csv",
        "data/ad_data.csv",
        "../recruitment/fv-sec-001-software-engineer-challenge/ad_data.csv",
        "ad_data.csv",
        "..\\recruitment\\fv-sec-001-software-engineer-challenge\\ad_data.csv"
    ]
    
    filepath = None
    for c in candidates:
        if os.path.exists(c):
            filepath = c
            break
            
    if not filepath:
        print("Lỗi: Không tìm thấy file ad_data.csv. Vui lòng kiểm tra lại đường dẫn.")
        exit(1)
        
    num_lines = 50000 
    
    print("-" * 60)
    print(f"BẮT ĐẦU TEST SO SÁNH STREAM vs BUFFERED STREAM ({num_lines} DÒNG)")
    print("-" * 60)
    
    print("\n1. Đang chạy BUFFERED STREAM...")
    buf_time = test_buffered_stream(filepath, num_lines)
    print(f"   => Hoàn thành trong: {buf_time:.4f} giây")
    
    print("\n2. Đang chạy UNBUFFERED STREAM (Từng byte từ ổ cứng)...")
    unbuf_time = test_unbuffered_stream(filepath, num_lines)
    print(f"   => Hoàn thành trong: {unbuf_time:.4f} giây\n")
    
    ratio = unbuf_time / buf_time if buf_time > 0 else 0
    print("=" * 60)
    print(f"KẾT LUẬN: Buffered Stream NHANH GẤP ~{ratio:.0f} LẦN stream thông thường.")
    print("=" * 60)
