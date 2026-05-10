# TEST REPORT
## Hệ thống Quản lý Phòng khám – Clinic Management System

---

| Thông tin | Chi tiết |
|:--|:--|
| **Tên dự án** | Clinic Management System |
| **Tên tài liệu** | Test Report – Báo cáo Kết quả Kiểm thử |
| **Phiên bản** | 1.0 |
| **Ngày lập báo cáo** | 09/05/2026 |
| **Người lập báo cáo** | Nhóm 1 – Ngô Hoàng Kiều Trang, Nguyễn Thanh Nhi |
| **Giảng viên hướng dẫn** | ThS. Võ Việt Khoa |
| **Môn học** | Kiểm thử Phần mềm – Lớp IM2301 |

---

## 1. Giới thiệu

### 1.1. Mục đích tài liệu

Tài liệu Test Report này trình bày kết quả kiểm thử chính thức của hệ thống Clinic Management System, bao gồm toàn bộ hoạt động kiểm thử đã được thực hiện, kết quả đạt được, lỗi phát hiện và đánh giá tổng thể chất lượng hệ thống.

Báo cáo được lập dựa trên kết quả thực thi các test case đã thiết kế trong Test Plan, nhằm:

- Lưu lại kết quả kiểm thử phần mềm một cách có tổ chức
- Mô tả điều kiện và môi trường kiểm thử
- So sánh kết quả kiểm thử với mục tiêu kiểm thử đề ra
- Đánh giá tổng thể mức độ hoàn thiện và chất lượng của hệ thống

### 1.2. Tổng quan hệ thống

Clinic Management System là hệ thống quản lý phòng khám hỗ trợ số hóa quy trình khám chữa bệnh. Hệ thống phục vụ ba nhóm người dùng chính:

- **Bệnh nhân**: Đặt lịch khám trực tuyến, thanh toán đặt cọc, xem lịch sử khám bệnh, đơn thuốc, kết quả xét nghiệm và đánh giá bác sĩ.
- **Bác sĩ**: Xem lịch khám, ghi chẩn đoán, kê đơn thuốc, yêu cầu xét nghiệm và hoàn tất ca khám.
- **Admin**: Quản lý thông tin bác sĩ, chuyên khoa và danh mục thuốc theo mô hình CRUD.

Hệ thống được xây dựng theo kiến trúc Client-Server, sử dụng Flask (Python) làm backend RESTful API, MySQL làm cơ sở dữ liệu và giao diện frontend bằng HTML/CSS/JavaScript thuần.

---

## 2. Phạm vi kiểm thử

### 2.1. Phạm vi thực hiện

Kiểm thử tập trung vào kiểm thử chức năng (Functional Testing) cho các module sau:

| STT | Module | Loại kiểm thử |
|:--:|:--|:--|
| 1 | Authentication Module | Unit Testing, Manual Testing |
| 2 | Appointment Module | Unit Testing, Manual Testing |
| 3 | Payment Module | Unit Testing |
| 4 | Examination Module | Unit Testing, Manual Testing |
| 5 | Prescription Module | Unit Testing, Manual Testing |
| 6 | LabTest Module | Unit Testing, Manual Testing |
| 7 | Medical History Module | Unit Testing |
| 8 | Review Module | Unit Testing, Manual Testing |
| 9 | Doctor Module | Unit Testing, Manual Testing |
| 10 | Specialty Module | Manual Testing |
| 11 | Medicine Module | Manual Testing |
| 12 | Patient Module | Unit Testing |

### 2.2. Phạm vi không thực hiện

Các loại kiểm thử sau **không** được triển khai trong phạm vi đồ án này do giới hạn về thời gian, nhân lực và trình độ chuyên môn:

- Automation Testing
- Performance Testing / Load Testing / Stress Testing
- Cross-browser Automation Testing
- Continuous Integration Testing

---

## 3. Môi trường kiểm thử

### 3.1. Phần cứng

| Thành phần | Cấu hình |
|:--|:--|
| CPU | Intel Core i5 hoặc tương đương |
| RAM | 8GB trở lên |
| Storage | SSD 256GB trở lên |
| Thiết bị kiểm thử | Máy tính cá nhân |

### 3.2. Phần mềm

| Thành phần | Mô tả |
|:--|:--|
| Hệ điều hành | Windows 10/11 hoặc macOS |
| Trình duyệt kiểm thử | Google Chrome, Microsoft Edge |
| Backend Framework | Flask (Python) |
| Database | MySQL |
| API Testing Tool | Postman |
| Admin Framework | Flask-Admin |

### 3.3. Công cụ hỗ trợ kiểm thử

| Công cụ | Mục đích sử dụng |
|:--|:--|
| Pytest | Thực hiện Unit Testing |
| Postman | Kiểm thử API |
| Google Chrome DevTools | Debug giao diện và kiểm tra dữ liệu |
| Google Sheets | Quản lý test case và bug list |

---

## 4. Kết quả Kiểm thử Đơn vị (Unit Testing)

### 4.1. Tổng quan

Unit Testing được thực hiện bằng framework **pytest**, tập trung kiểm tra tính đúng đắn của các API endpoint, business logic, validation logic, role authorization và các luồng xử lý nghiệp vụ chính của từng module.

Môi trường kiểm thử: **localhost (phát triển cục bộ)**, các thành phần phụ thuộc được mock/giả lập để cô lập đối tượng kiểm thử.

### 4.2. Kết quả Unit Testing theo module

Bộ test được tổ chức thành các file test tương ứng với từng module chức năng.
Kết quả được đo lường bằng **pytest** kết hợp **coverage.py v7.13.5**,
thực hiện ngày 08/05/2026.

| STT | Module | File kiểm thử | Số statements | Tỷ lệ Coverage |
|:--:|:--|:--|:--:|:--:|
| 1 | Authentication – Login | `test_auth/test_login.py` | 25 | 100% |
| 2 | Authentication – Register | `test_auth/test_register.py` | 49 | 100% |
| 3 | Authentication – Security | `test_auth/test_security.py` | 7 | 100% |
| 4 | Menu Bar | `test_auth/test_menu_bar.py` | 43 | 100% |
| 5 | Appointment (Patient) | `test_patient/test_appointment_patient.py` | 212 | 100% |
| 6 | Payment Module | `test_patient/test_payment.py` | 115 | 100% |
| 7 | Medical History | `test_patient/test_medical_history.py` | 127 | 100% |
| 8 | Review Module | `test_patient/test_review.py` | 121 | 100% |
| 9 | Patient Profile | `test_patient/test_profile_patient.py` | 178 | 100% |
| 10 | Guest (Public) | `test_patient/test_guest.py` | 16 | 100% |
| 11 | Appointment (Doctor) | `test_doctor/test_appointment_doctor.py` | 138 | 99% |
| 12 | Examination Module | `test_doctor/test_examination.py` | 179 | 100% |
| 13 | LabTest Module | `test_doctor/test_lab.py` | 129 | 100% |
| 14 | Prescription Module | `test_doctor/test_prescription.py` | 124 | 100% |
| 15 | Doctor Profile | `test_doctor/test_profile_doctor.py` | 91 | 100% |
| 16 | Utility Functions | `test_func.py` | 22 | 100% |

#### Độ bao phủ mã nguồn toàn dự án

| File | Statements | Missing | Coverage |
|:--|:--:|:--:|:--:|
| `app\admin.py` | 82 | 23 | 72% |
| `app\app.py` | 30 | 8 | 73% |
| `app\config\config.py` | 22 | 0 | 100% |
| `app\initialize_functions.py` | 28 | 5 | 82% |
| `app\models\appointment.py` | 25 | 2 | 92% |
| `app\models\examination.py` | 12 | 0 | 100% |
| `app\models\payment.py` | 19 | 2 | 89% |
| `app\models\prescription.py` | 23 | 0 | 100% |
| `app\models\review.py` | 19 | 1 | 95% |
| `app\models\schedule.py` | 22 | 0 | 100% |
| `app\models\specialization.py` | 11 | 1 | 91% |
| `app\models\status.py` | 33 | 0 | 100% |
| `app\models\test.py` | 18 | 0 | 100% |
| `app\models\users.py` | 52 | 4 | 92% |
| `app\modules\doctor\dao.py` | 280 | 7 | 98% |
| `app\modules\doctor\routes.py` | 237 | 8 | 97% |
| `app\modules\patient\dao.py` | 192 | 4 | 98% |
| `app\modules\patient\routes.py` | 213 | 2 | 99% |
| `app\modules\user\dao.py` | 38 | 0 | 100% |
| `app\modules\user\routes.py` | 27 | 0 | 100% |
| `app\modules\web\routes.py` | 35 | 11 | 69% |
| `app\seed_data.py` | 222 | 201 | 9%* |
| `app\tests\conftest.py` | 233 | 0 | 100% |
| **Tổng toàn dự án** | **3499** | **284** | **92%** |

> \* `seed_data.py` là script khởi tạo dữ liệu mẫu, không nằm trong phạm vi
> kiểm thử chức năng nên tỷ lệ coverage thấp (9%) là chấp nhận được.

#### Tổng kết độ bao phủ mã nguồn

| Tiêu chí | Mục tiêu (Test Plan) | Kết quả thực tế |
|:--|:--:|:--:|
| Line Coverage toàn dự án | ≥ 70% |  **92%** |
| Coverage các module nghiệp vụ chính | ≥ 70% |  **97–100%** |
| Test files coverage | 100% |  Đạt (hầu hết 100%) |

Kết quả **92% line coverage** trên tổng 3.499 statements vượt mục tiêu đề ra
(≥ 70%), đặc biệt các module nghiệp vụ cốt lõi như `doctor/dao.py` (98%),
`patient/routes.py` (99%), `doctor/routes.py` (97%) đều đạt tỷ lệ bao phủ
rất cao.

### 4.3. Độ bao phủ mã nguồn (Code Coverage)

| Tiêu chí | Mục tiêu | Kết quả đạt được |
|:--|:--:|:--:|
| Line Coverage | ≥ 70% |  Đạt |
| Function Coverage | ≥ 70% |  Đạt |

Kết quả bao phủ mã nguồn được đo lường sau khi thực thi toàn bộ test suite bằng pytest-cov. Hệ thống đạt mức bao phủ đáp ứng tiêu chí đề ra trong Test Plan.

### 4.4. Phân loại test case theo kịch bản

| Loại kịch bản | Số lượng TC | Passed | Failed |
|:--|:--:|:--:|:--:|
| Normal Case (hợp lệ) | 100 | 100 | 0 |
| Negative Case (không hợp lệ) | 123 | 123 | 0 |
| Boundary Case (biên) | 29 | 29 | 0 |
| Authorization Testing (phân quyền) | 64 | 64 | 0 |
| **Tổng** | **316** | **316** | **0** |

---

## 5. Kết quả Kiểm thử Thủ công (Manual Functional Testing)

### 5.1. Tổng quan

Kiểm thử thủ công được thực hiện trên môi trường **localhost** thông qua trình duyệt Google Chrome và Microsoft Edge. Các test case được thực thi theo từng nhóm người dùng, bao phủ các luồng nghiệp vụ chính của hệ thống.

Toàn bộ test case thủ công được quản lý qua **Google Sheets**, theo dõi theo ba trạng thái: `Passed`, `Failed`, `Blocked`.

### 5.2. Phạm vi kiểm thử thủ công

Các chức năng được kiểm thử thủ công bao gồm:

**Nhóm Bệnh nhân:**
- Đặt lịch khám trực tuyến
- Thanh toán đặt cọc
- Xem lịch hẹn và lịch sử khám bệnh
- Đánh giá bác sĩ

**Nhóm Bác sĩ:**
- Xem và quản lý lịch khám
- Khám bệnh và ghi chẩn đoán
- Kê đơn thuốc
- Quản lý yêu cầu xét nghiệm

**Nhóm Admin:**
- Quản lý bác sĩ (CRUD)
- Quản lý chuyên khoa (CRUD)
- Quản lý thuốc (CRUD)

### 5.3. Kết quả kiểm thử thủ công theo module

| STT | Module | Tổng TC | Passed | Failed | Blocked | Tỷ lệ Pass |
|:--:|:--|:--:|:--:|:--:|:--:|:--:|
| 1 | AUTH | 14 | 14 | 0 | 0 | 100% |
| 2 | PATIENT | 13 | 13 | 0 | 0 | 100% |
| 3 | DOCTOR | 13 | 13 | 0 | 0 | 100% |
| 4 | ADMIN | 19 | 19 | 0 | 0 | 100% |
| 5 | E2E | 10 | 10 | 0 | 0 | 100% |
| **Tổng** | | **69** | **69** | **0** | **0** | **100%** |

---

## 6. Kết quả Kiểm thử Tích hợp (Integration Testing)

### 6.1. Tổng quan

Kiểm thử tích hợp được thực hiện dưới hình thức **Manual End-to-End (E2E) Testing**, kiểm tra toàn bộ luồng nghiệp vụ xuyên suốt từ đầu đến cuối, đảm bảo dữ liệu được đồng bộ chính xác giữa các module và các vai trò người dùng.

Công cụ sử dụng: **Postman** (kiểm thử API), **Google Chrome DevTools** (kiểm tra dữ liệu phản hồi).

### 6.2. Kết quả theo kịch bản tích hợp

| STT | Kịch bản tích hợp | Kết quả | Ghi chú |
|:--:|:--|:--:|:--|
| 1 | Đặt lịch → Thanh toán → Khám bệnh → Kê đơn → Xem kết quả |  Passed | Luồng chính hoạt động đúng |
| 2 | Thanh toán thất bại và xử lý trạng thái lịch hẹn |  Passed | Trạng thái cập nhật chính xác |
| 3 | Đồng bộ lịch khám giữa bệnh nhân và bác sĩ |  Passed | Dữ liệu nhất quán |
| 4 | Hiển thị kết quả khám sau khi hoàn tất ca khám |  Passed | Bệnh nhân xem được đúng kết quả |
| 5 | Xử lý khi dữ liệu khám chưa hoàn tất |  Passed | Thông báo phù hợp |
| 6 | Nhiều bệnh nhân đặt cùng một khung giờ |  Passed *(cần lưu ý)* | Hệ thống xử lý đúng nhưng cần kiểm tra thêm ở tải cao |
| 7 | Lưu trạng thái dữ liệu khi refresh hệ thống |  Passed | Dữ liệu được giữ nguyên |

**Tổng kết:** 7/7 kịch bản tích hợp Passed (100%)

---

## 7. Kết quả Kiểm thử Hệ thống (System Testing)

### 7.1. Tổng quan

Kiểm thử hệ thống được thực hiện sau khi toàn bộ các phân hệ đã được tích hợp, đánh giá hệ thống như một sản phẩm hoàn chỉnh theo các tình huống sử dụng thực tế của từng nhóm người dùng.

Phương thức thực hiện: **Manual End-to-End Testing** trên môi trường phát triển cục bộ (localhost).

### 7.2. Kết quả theo luồng nghiệp vụ hệ thống

| STT | Luồng nghiệp vụ | Kết quả | Ghi chú |
|:--:|:--|:--:|:--|
| 1 | Đặt lịch khám và thanh toán đặt cọc |  Passed | Hoạt động đúng theo yêu cầu |
| 2 | Khám bệnh và lưu kết quả khám |  Passed | Dữ liệu lưu đầy đủ |
| 3 | Kê đơn thuốc và yêu cầu xét nghiệm |  Passed | |
| 4 | Xem lịch sử khám bệnh |  Passed | Hiển thị chính xác |
| 5 | Đánh giá bác sĩ sau khám |  Passed | |
| 6 | Quản lý dữ liệu hệ thống của Admin |  Passed | CRUD hoạt động đúng |

**Tổng kết:** 6/6 luồng nghiệp vụ hệ thống Passed (100%)

---

## 8. Danh sách Lỗi Phát hiện (Defect Report)

### 8.1. Tổng hợp lỗi theo mức độ nghiêm trọng

| Mức độ | Số lượng | Đã xử lý | Còn tồn đọng |
|:--|:--:|:--:|:--:|
| Critical | 0 | 0 | 0 |
| High | 2 | 2 | 2 |
| Medium | 8 | 8 | 0 |
| Low | 5 | 4 | 1 |
| **Tổng** | **15** | **14** | **1** |

### 8.2. Chi tiết các lỗi phát hiện

| Bug ID | Module | Mô tả lỗi | Mức độ | Trạng thái |
|:--|:--|:--|:--:|:--:|
| BUG-001 | Appointment | Hệ thống cho phép đặt lịch với ngày trong quá khứ khi truyền trực tiếp qua API (bypass validation phía client) | High | Fixed |
| BUG-002 | Payment | Trạng thái lịch hẹn không cập nhật sang `pending` ngay sau khi thanh toán thành công trong một số trường hợp race condition | High | Fixed |
| BUG-003 | Prescription | Có thể thêm thuốc vào đơn thuốc của lịch hẹn đã hoàn tất (status = `completed`) | Medium | Fixed |
| BUG-004 | Appointment | Cho phép xem đơn thuốc khi trạng thái chưa hoàn tất (status != `completed`) | Medium | Fixed |
| BUG-005 | Review | Hệ thống cho phép bệnh nhân gửi đánh giá trùng lặp cho cùng một lịch hẹn trong một số trường hợp | Medium | Fixed |
| BUG-006 | Doctor (Admin) | Khi xóa bác sĩ đang có lịch hẹn chưa hoàn tất, hệ thống không hiển thị cảnh báo phù hợp | Medium | Fixed |
| BUG-007 | Examination | Cho phép hoàn tất khám bệnh khi lab test chưa hoàn tất | Medium | Fixed |
| BUG-008 | Patient | Trường `date_of_birth` cho phép cập nhật với giá trị ngày tương lai | Medium | Fixed |
| BUG-009 | Medicine (Admin) | Cho phép giá thuốc âm | Low | Fixed |
| BUG-010 | Payment | UI không hiển thị thông báo khi thanh toán thành công/thất bại | Low | Fixed |
| BUG-011 | Examination | Không validate độ dài tối đa của trường `diagnosis` khi gọi API trực tiếp | Low | Open |
| BUG-012 | Payment | Chưa tạo thanh toán Final có status = `paid` khi hoàn tất lịch khám | Low | Fixed |
| BUG-013 | Specialty | Trùng tên chuyên khoa (case-insensitive) không được kiểm tra đầy đủ | Low | Fixed |
| BUG-014 | Appointment | Không chuyển sang trạng thái `in_progress` khi tạo đơn khám bệnh | Medium | Fixed |
| BUG-015 | Review | Cho phép đánh giá khi không nhập rating | Medium | Fixed |

---

## 9. Tổng kết Kết quả Kiểm thử

### 9.1. Tổng hợp toàn bộ hoạt động kiểm thử

| Loại kiểm thử | Tổng TC | Passed | Failed | Tỷ lệ Pass |
|:--|:--:|:--:|:--:|:--:|
| Unit Testing | 316 | 316 | 316 | 100% |
| Manual Functional Testing | 79 | 79 | 0 | 100% |
| Integration Testing (E2E) | 7 | 7 | 0 | 100% |
| System Testing (E2E) | 6 | 6 | 0 | 100% |
| **Tổng cộng** | **408** | **408** | **0** | **100%** |

### 9.2. Điều kiện kết thúc kiểm thử (Exit Criteria)

| Tiêu chí | Kết quả |
|:--|:--:|
| Tất cả test case đã được thực thi |  Đạt |
| Kết quả kiểm thử đã được ghi nhận đầy đủ |  Đạt |
| Không còn lỗi Critical |  Đạt |
| Các lỗi High đã được xử lý |  Đạt (2/2) |
| Các luồng nghiệp vụ chính hoạt động ổn định |  Đạt |
| Unit Testing đạt yêu cầu bao phủ mã nguồn (≥ 70%) |  Đạt |
| Integration Testing và E2E Testing hoạt động đúng |  Đạt |
| Dữ liệu giữa các module được đồng bộ chính xác |  Đạt |

---

## 10. Đánh giá Chất lượng Hệ thống

### 10.1. Điểm mạnh

- Các luồng nghiệp vụ chính (đặt lịch → thanh toán → khám bệnh → kê đơn → xem kết quả) hoạt động đúng và đồng bộ giữa các vai trò người dùng.
- Cơ chế xác thực JWT và phân quyền hoạt động ổn định; các trường hợp truy cập trái phép đều bị từ chối đúng quy định.
- Validation dữ liệu đầu vào ở tầng API đáp ứng tốt cho các trường hợp thông thường.
- Các module Admin (quản lý bác sĩ, chuyên khoa, thuốc) hoạt động chính xác theo mô hình CRUD.
- Độ bao phủ mã nguồn đạt yêu cầu đề ra (Line Coverage ≥ 70%, Function Coverage ≥ 70%).

### 10.2. Điểm cần cải thiện

- Một số trường hợp **Negative Testing** qua API trực tiếp (bypass giao diện) vẫn chưa được xử lý chặt chẽ ở phía server, đặc biệt liên quan đến validation ngày tháng và độ dài chuỗi.
- Còn **1 lỗi Open** ở mức Low cần được xử lý trong phiên bản tiếp theo.
- Giao diện chưa có cơ chế tự động reload/thông báo real-time sau các thao tác quan trọng (ví dụ: BUG-012).
- Cần bổ sung kiểm tra trùng lặp không phân biệt hoa/thường (case-insensitive) cho một số trường như tên chuyên khoa.

### 10.3. Rủi ro tồn đọng

| Rủi ro | Mức độ | Ghi chú |
|:--|:--:|:--|
| 1 lỗi Open chưa được xử lý | Low| Không ảnh hưởng đến luồng nghiệp vụ chính |
| Chưa thực hiện Performance Testing | Trung bình | Chưa đánh giá được khả năng chịu tải |
| Chưa có Automation Testing | Trung bình | Regression Testing phải thực hiện thủ công |

---

## 11. Kết luận và Kiến nghị

### 11.1. Kết luận

Quá trình kiểm thử hệ thống Clinic Management System đã hoàn tất toàn bộ các giai đoạn theo kế hoạch, bao gồm Unit Testing, Manual Functional Testing, Integration Testing và System Testing.

Kết quả tổng thể cho thấy hệ thống hoạt động đúng theo yêu cầu nghiệp vụ với tỷ lệ pass đạt **94.2%** trên tổng số 260 test case. Tất cả các luồng nghiệp vụ chính đều hoạt động ổn định. Không có lỗi Critical; các lỗi High đã được xử lý hoàn toàn. Hệ thống đủ điều kiện bàn giao theo tiêu chí Exit Criteria đã đề ra trong Test Plan.

### 11.2. Kiến nghị

1. **Ưu tiên xử lý 1 lỗi Open** và thực hiện kiểm thử chuyên sâu hơn để phát hiện các lỗi tiềm ẩn khác.
2. **Bổ sung server-side validation** chặt chẽ hơn cho các trường dữ liệu nhạy cảm (ngày tháng, độ dài chuỗi) để phòng trường hợp bypass qua API.
3. **Triển khai Automation Testing** (Regression Testing, UI Testing với Selenium) trong tương lai nhằm tăng hiệu quả kiểm thử khi hệ thống mở rộng.
4. **Thực hiện Performance Testing** để đánh giá khả năng chịu tải của hệ thống trong điều kiện nhiều người dùng đồng thời.
5. **Tăng cường kiểm thử bảo mật** (Security Testing) đặc biệt đối với các dữ liệu y tế nhạy cảm của bệnh nhân. Hiện tại chỉ kiểm thử SQL Injection khi login và register, chưa thực hiện kiểm thử chueyen sâu.

---
**Ngày hoàn thành:** 10/05/2026