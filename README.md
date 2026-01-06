URL & File Security Scanner🛡️

Một web application mạnh mẽ giúp kiểm tra URL hoặc file có chứa mã độc, phishing hay rủi ro bảo mật không, sử dụng VirusTotal API.
Dự án được viết bằng Python Flask, hỗ trợ lưu lịch sử scan bằng SQLite.

Tính năng chính:

🔗 Kiểm tra URL – Dán link để xem có bị đánh dấu là malicious/phishing không.

📁 Upload file để scan – Hỗ trợ mọi loại file (tối đa 32MB), file chỉ lưu tạm và tự động xóa sau khi scan.

📊 Lịch sử scan – Xem lại tất cả các lần kiểm tra trước đó (thời gian, loại, mục tiêu, kết quả, số lượng phát hiện).

🎨 Giao diện dễ nhìn, dễ sử dụng.

🛡️ An toàn & riêng tư – Không lưu file lâu dài, database chỉ lưu metadata.

*Demo (chạy local)

-Trang chính
<img width="1555" height="806" alt="{8297EE18-78EE-4F53-BA2C-6776E4F81B94}" src="https://github.com/user-attachments/assets/505d59d3-f94a-4088-ab29-a1313c7182e2" />

-Lịch sử scan
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/389edfa4-924b-415b-aa91-7cc49ae9cc1a" />

*Yêu cầu hệ thống:

-Python 3.8 trở lên

-Kết nối Internet (để gọi VirusTotal API)

-Cài đặt & chạy dự án:

-git clone https://github.com/whoisry4n/url-file-security-scanner.git

-cd url-file-security-scanner

-pip install flask requests werkzeug

-Lấy API key từ VirusTotal

-Đăng ký miễn phí tại: https://www.virustotal.com/gui/join-us

-Vào My API key để copy key.

-Thay API key vào code

-Mở file app.py, tìm dòng: PythonVIRUSTOTAL_API_KEY = 'YOUR_API_KEY_HERE'Thay 'YOUR_API_KEY_HERE' bằng key thật của bạn.

-python app.py

-Mở trình duyệt và vào: http://127.0.0.1:5000

*Cấu trúc dự án

url-file-security-scanner/

├── app.py                  # Code chính Flask

├── scans.db                # Database SQLite (tự tạo khi chạy lần đầu)

├── uploads/                # Thư mục tạm lưu file upload (tự xóa sau scan)

├── templates/

│   ├── index.html          # Trang chính (scan URL/file)

│   └── history.html        # Trang lịch sử scan

├── .gitignore

└── README.md               # Tài liệu này

*Lưu ý khi sử dụng

-API key miễn phí của VirusTotal có giới hạn (500 request/ngày, 4 request/phút cho file).

-File upload tối đa 32MB (giới hạn API public).

-Ứng dụng chạy local nên hoàn toàn riêng tư.

*Tác giả:

-Nhóm SV an ninh mạng.

-Dự án thực hiện theo yêu cầu môn CDIO - CS 447.

*License

-MIT License.
