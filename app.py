from flask import Flask, render_template, request
import requests
import os
import time
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Thư mục tạm để lưu file upload
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Giới hạn file 32MB

# API key thực từ VirusTotal (virustotal.com)
VIRUSTOTAL_API_KEY = 'YOUR_API_KEY_HERE'

# Khởi tạo database SQLite
DB_FILE = 'scans.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            type TEXT NOT NULL,  -- 'URL' hoặc 'File'
            target TEXT NOT NULL,  -- URL hoặc tên file
            result TEXT NOT NULL,
            positives INTEGER,
            total INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Hàm insert lịch sử scan
def insert_scan(type, target, result, positives, total):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO scans (timestamp, type, target, result, positives, total)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, type, target, result, positives, total))
    conn.commit()
    conn.close()

# Hàm xóa file tạm sau khi sử dụng
def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'url' in request.form and request.form['url']:  # Kiểm tra URL
            url_to_check = request.form['url']
            scan_result = scan_url(url_to_check)
            if 'Lỗi' not in scan_result:  # Chỉ lưu nếu thành công
                positives, total = extract_positives_total(scan_result)
                insert_scan('URL', url_to_check, scan_result, positives, total)
            result = scan_result
        
        elif 'file' in request.files:  # Kiểm tra file
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    scan_result = scan_file(filepath)
                    if 'Lỗi' not in scan_result:  # Chỉ lưu nếu thành công
                        positives, total = extract_positives_total(scan_result)
                        insert_scan('File', filename, scan_result, positives, total)
                    result = scan_result
                finally:
                    delete_file(filepath)  # Xóa file sau khi scan
                
            else:
                result = 'Vui lòng chọn file để kiểm tra.'
    
    return render_template('index.html', result=result)

def extract_positives_total(result):
    # Trích xuất positives và total từ string result (ví dụ: "URL có rủi ro! 5/60 ...")
    if 'an toàn' in result:
        return 0, 0  # Mặc định cho an toàn
    else:
        try:
            parts = result.split('! ')[1].split('/')[0:2]
            positives = int(parts[0])
            total = int(parts[1].split(' ')[0])
            return positives, total
        except (IndexError, ValueError):  # Sửa ở đây: thêm loại lỗi cụ thể
            return None, None

def scan_url(url):
    vt_url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = {'apikey': VIRUSTOTAL_API_KEY, 'url': url}
    response = requests.post(vt_url, data=params)
    
    if response.status_code == 200:
        scan_id = response.json().get('scan_id')
        
        # Chờ 10 giây để VirusTotal xử lý (có thể tăng nếu cần)
        time.sleep(10)
        
        report_url = 'https://www.virustotal.com/vtapi/v2/url/report'
        report_params = {'apikey': VIRUSTOTAL_API_KEY, 'resource': scan_id}
        report_response = requests.get(report_url, params=report_params)
        
        if report_response.status_code == 200:
            report = report_response.json()
            positives = report.get('positives', 0)
            total = report.get('total', 0)
            
            if positives > 0:
                return f'URL có rủi ro! {positives}/{total} công cụ phát hiện mã độc hoặc lừa đảo.'
            else:
                return 'URL an toàn theo VirusTotal.'
        else:
            return 'Lỗi khi lấy báo cáo URL. Thử lại sau.'
    else:
        return 'Lỗi khi quét URL. Kiểm tra API key hoặc kết nối.'

def scan_file(filepath):
    vt_url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': VIRUSTOTAL_API_KEY}
    files = {'file': (os.path.basename(filepath), open(filepath, 'rb'))}
    response = requests.post(vt_url, files=files, params=params)
    
    if response.status_code == 200:
        scan_id = response.json().get('scan_id')
        
        # Chờ 30 giây để VirusTotal scan file (có thể cần lâu hơn cho file lớn)
        time.sleep(30)
        
        report_url = 'https://www.virustotal.com/vtapi/v2/file/report'
        report_params = {'apikey': VIRUSTOTAL_API_KEY, 'resource': scan_id}
        report_response = requests.get(report_url, params=report_params)
        
        if report_response.status_code == 200:
            report = report_response.json()
            if report.get('response_code') == -2:  # Nếu đang queue, chờ thêm
                time.sleep(30)
                report_response = requests.get(report_url, params=report_params)
                report = report_response.json()
            
            positives = report.get('positives', 0)
            total = report.get('total', 0)
            
            if positives > 0:
                return f'File có rủi ro! {positives}/{total} công cụ phát hiện mã độc hoặc lừa đảo.'
            else:
                return 'File an toàn theo VirusTotal.'
        else:
            return 'Lỗi khi lấy báo cáo file. Thử lại sau.'
    else:
        return 'Lỗi khi quét file. Kiểm tra API key, kích thước file hoặc kết nối.'

@app.route('/history')
def history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scans ORDER BY id DESC LIMIT 50')  # Lấy 50 mới nhất
    scans = cursor.fetchall()
    conn.close()
    return render_template('history.html', scans=scans)

if __name__ == '__main__':
    init_db()  # Khởi tạo DB khi chạy app
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)