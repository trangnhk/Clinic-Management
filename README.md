# Clinic-Management

## Mô tả
Clinic Management System là hệ thống quản lý phòng khám được phát triển nhằm hỗ trợ quá trình khám chữa bệnh và quản lý thông tin y tế một cách hiệu quả, giảm thời gian chờ đợi của bệnh nhân và hỗ trợ bác sĩ trong quá trình khám bệnh.

Hệ thống cho phép bệnh nhân đặt lịch khám trực tuyến, thanh toán đặt cọc, xem lịch sử khám bệnh, đơn thuốc và kết quả xét nghiệm. Bác sĩ có thể xem lịch khám, ghi chẩn đoán, kê đơn thuốc và yêu cầu xét nghiệm. Admin quản lý thông tin bác sĩ, chuyên khoa và danh mục thuốc trong hệ thống.

Hệ thống được xây dựng với mục tiêu cải thiện trải nghiệm người dùng, tăng hiệu quả quản lý phòng khám và hỗ trợ lưu trữ dữ liệu y tế một cách chính xác và thuận tiện.

## Thành viên nhóm
| Thành viên | MSSV | Vai trò |
|------------|------|-----------|
| Ngô Hoàng Kiều Trang | 2354050141 | Project Manager và Developer chính |
| Nguyễn Thanh Nhi | 2251010067 | QA/Tester và Developer |

## Công nghệ sử dụng
- Backend: Flask
- Frontend: Javascript, HTML thuần
- Database: MySQL

## Cài đặt và chạy

### Yêu cầu:
- Python 3.10+
- MySQL: database clinicdb

### Chạy project
cd backend\src

pip install -r requirements.txt

app\run_project.bat

### Truy cập
http://localhost:5000

## Demo
[![Watch the video](/docs/demo/demo.png)](/docs/demo/demo.mp4)

## Tài liệu
- [Phân tích yêu cầu](/docs/requirements.md)
- [Test Plan](/docs/test_plan.md)
- [Test Report](/docs/test-report.md)