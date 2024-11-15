📅 Hệ Thống Tự Động Phân Thời Khóa Biểu Cho Trường THPT
Đây là hệ thống tự động phân lịch học cho giáo viên và học sinh tại trường trung học phổ thông, sử dụng Python và Flask. Hệ thống có thể tạo ra thời khóa biểu tối ưu, giảm thiểu xung đột và phù hợp với các ràng buộc thời gian của cả giáo viên và học sinh.

📋 Mục tiêu
Tự động hóa phân thời khóa biểu cho các lớp học và giáo viên.
Dễ sử dụng: Giao diện đơn giản, hỗ trợ người dùng dễ dàng truy cập, chỉnh sửa và quản lý lịch.
Tối ưu hóa thời gian học: Giảm thiểu xung đột lịch và sắp xếp hợp lý theo các ràng buộc thời gian.
🎯 Tính năng chính
Phân lịch tự động dựa trên các yêu cầu của môn học, giáo viên và các lớp.
Giao diện quản trị cho phép quản trị viên phân lịch, xem và chỉnh sửa lịch.
Trang cá nhân cho giáo viên và học sinh để xem thời khóa biểu.
Phát hiện xung đột trong lịch giảng dạy và học tập.
🛠️ Công nghệ sử dụng
Ngôn ngữ lập trình: HTML; Python; JS
Web Framework: Flask
Thư viện xử lý dữ liệu: pandas
Logging: Tích hợp logging để ghi nhận và theo dõi các thao tác và lỗi
Cơ sở dữ liệu: Sử dụng file Excel (school_schedule_data.xlsx) để lưu trữ dữ liệu về giáo viên, lớp học và lịch.
📦 Cài đặt
Yêu cầu hệ thống
Python 3.7+
Flask (có thể cài đặt từ requirements.txt)
Pandas (để xử lý dữ liệu từ file Excel)
Hướng dẫn cài đặt
Clone repository:

git clone https://github.com/yourusername/school-schedule-system.git
cd school-schedule-system
Cài đặt các thư viện yêu cầu:

pip install -r requirements.txt
Thiết lập biến môi trường (tùy chọn):

Trong file .env, thiết lập FLASK_SECRET_KEY để bảo mật phiên làm việc Flask.
Hoặc có thể đặt trực tiếp trong mã với giá trị mặc định your_secret_key.
Chuẩn bị file dữ liệu Excel:

Đảm bảo rằng file school_schedule_data.xlsx có các sheet sau: teachers, teacher_schedule, classes, class_schedule, subject_schedule.
Chạy ứng dụng:

python app.py
Truy cập ứng dụng:

Ứng dụng sẽ chạy tại http://localhost:5000.
🚀 Hướng dẫn sử dụng
Đăng nhập:

Truy cập vào http://localhost:5000/login.
Sử dụng tài khoản quản trị (admin/admin123 mặc định) hoặc tài khoản giáo viên, học sinh đã được thêm trong file Excel.
Trang quản trị:

Đăng nhập bằng tài khoản quản trị viên để vào Bảng điều khiển quản trị.
Tại đây, bạn có thể xem, chỉnh sửa thời khóa biểu hoặc phân lịch tự động.
Phân lịch tự động: Nhấn nút "Phân lịch tự động" để hệ thống tự động phân lịch cho giáo viên và các lớp.
Trang cá nhân của giáo viên và học sinh:

Giáo viên và học sinh có thể đăng nhập để xem lịch của riêng mình.
Đăng xuất:

Truy cập http://localhost:5000/logout để đăng xuất.
🧩 Cấu trúc thư mục
app.py - File chính của ứng dụng Flask.
templates/ - Chứa các file HTML cho giao diện web.
static/ - Chứa các file tĩnh như CSS và JavaScript.
school_schedule_data.xlsx - File dữ liệu Excel chứa thông tin về giáo viên, lớp học và lịch học.
requirements.txt - Danh sách các thư viện cần thiết.
