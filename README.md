# URL & File Security Scanner 🛡️

- **Web application kiểm tra URL và file có chứa mã độc, phishing hoặc rủi ro bảo mật không, sử dụng VirusTotal API.**
- Dự án được xây dựng bằng **Python + Flask**, giao diện dễ nhìn & sử dụng, hỗ trợ lưu lịch sử scan bằng SQLite.

## Tính năng chính

- 🔗 **Kiểm tra URL** nhanh chóng – phát hiện malicious/phishing.
- 📁 **Upload file để scan** – hỗ trợ mọi định dạng (tối đa 32MB), file chỉ lưu tạm và tự động xóa ngay sau khi scan.
- 📊 **Lịch sử scan** – xem lại đầy đủ các lần kiểm tra trước đó (thời gian, loại, mục tiêu, kết quả, số lượng engine phát hiện).
- 🎨 **Giao diện đẹp mắt** – thân thiện với người dùng.
- 🔒 **An toàn & riêng tư** – không lưu file lâu dài, database chỉ chứa metadata.

## Ảnh minh họa

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1d2d56bc-7b2a-494c-879f-96e7f1551af6" />
  
*Giao diện trang chủ với form scan URL/file*

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c5b05bc3-a747-4542-b049-7d26a8e4d9a4" />

*Trang lịch sử scan với bảng chi tiết và phân màu an toàn/rủi ro*

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Kết nối Internet (để gọi VirusTotal API)

## Hướng dẫn cài đặt & chạy

1. **Clone repository**
   ```bash
   git clone https://github.com/whoisry4n/url-file-security-scanner.git
   cd url-checker
2. **Cài đặt các thư viện cần thiết**
   ```bash
   pip install flask requests
   pip install flask werkzeug
3. **Lấy API key từ VirusTotal**
   - Đăng ký tài khoản miễn phí tại: https://www.virustotal.com/gui/join-us
   - Vào phần My API key để copy key.
4. **Cấu hình API key**
   - Mở file app.py, tìm dòng: VIRUSTOTAL_API_KEY = 'YOUR_API_KEY_HERE'Thay 'YOUR_API_KEY_HERE' bằng API key thật của bạn.
5. **Chạy ứng dụng**
   ```bash
   python app.py
7. **Truy cập**
   - Mở trình duyệt và vào địa chỉ: http://127.0.0.1:5000

## Cấu trúc dự án
<img width="661" height="199" alt="{41184144-589B-4100-A7D0-89B225ACF372}" src="https://github.com/user-attachments/assets/feec1d8b-a4d1-4b18-9c11-44cb5febe193" />

## Lưu ý khi sử dụng

- API key miễn phí của VirusTotal giới hạn ~500 request/ngày và 4 request/phút đối với scan file.
- Kích thước file upload tối đa 32MB (giới hạn của API public).
- Ứng dụng chạy local nên hoàn toàn riêng tư và an toàn.

## Tác giả

- Nhóm SV an ninh mạng.
- Dự án thực hiện theo yêu cầu môn học CS-447.

## License
Dự án sử dụng MIT License – bạn được tự do sử dụng, chỉnh sửa và chia sẻ.
