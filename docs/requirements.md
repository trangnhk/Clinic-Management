# Phân tích yêu cầu

---
# 1. Phân tích yêu cầu chức năng
## 1.1 Bệnh nhân

**Đăng ký / Đăng nhập**
| ID | Yêu cầu |
|----|---------|
| FR-01 | Hệ thống phải cho phép bệnh nhân đăng ký tài khoản bằng email và mật khẩu |
| FR-02 | Hệ thống phải kiểm tra email không được trùng lặp |
| FR-03 | Hệ thống phải cho phép bệnh nhân đăng nhập |
| FR-04 | Hệ thống phải phân quyền theo vai trò người dùng dựa trên vai trò (Patien/Doctor/Admin) |

**Đặt lịch khám**
| ID | Yêu cầu |
|----|---------|
| FR-05 | Hệ thống phải hiển thị danh sách các chuyên khoa |
| FR-06 | Hệ thống phải hiện thị danh sách các bác sĩ theo chuyên khoa |
| FR-07 | Hệ thống phải hiển thị lịch trống của bác sĩ |
| FR-08 | Hệ thống phải cho phép bệnh nhân chọn ngày và giờ khám |
| FR-09 | Hệ thống không cho phép 2 bệnh nhân đặt trùng thời gian với cùng 1 bác sĩ|
| FR-10 | Hệ thống phải lưu thông tin lịch khám vào CSDL |
| FR-11 | Hệ thống phải cập nhật trạng thái lịch khám là "Pending Payment" khi bệnh nhân đặt lịch thành công  |

**Thanh toán đặt cọc**
| ID | Yêu cầu |
|----|---------|
| FR-12 | Hệ thống phải hiển thị thông tin đặt lịch trước khi thanh toán |
| FR-13 | Hệ thống phải ghi nhận trạng thái thanh toán |
| FR-14 | Hệ thống phải cập nhật trạng thái lịch khám là "Waiting Examination" khi thanh toán thành công |

**Xem lịch sử khám**
| ID | Yêu cầu |
|----|---------|
| FR-15 | Hệ thống phải hiển thị danh sách lịch khám của bệnh nhân |
| FR-16 | hệ thống phải cho phép bệnh nhân xem chi tiết lịch khám | 
| FR-17 | Hệ thống phải hiển thị chuẩn đoán của bác sĩ khi xem chi tiết lịch khám|
| FR-18 | Hệ thống phải hiển thị danh sách thuốc đã kê |

**Xem kết quả xét nghiệm**
| ID | Yêu cầu |
|----|---------|
| FR-19 | Hệ thống chỉ cho phép xem kết quả xét nghiệm khi trạng thái là "Done"|
| FR-20 | Hệ thống phải cho phép bệnh nhân xem chi tiết kết quả xét nghiệm |

**Đánh giá bác sĩ**
| ID | Yêu cầu |
|----|---------|
| FR-21 | Hệ thống phải cho phép bệnh nhân đánh giá bác sĩ sau khi hoàn thành khám với trạng thái lịch khám là "Completed" |
| FR-22 | Hệ thống phải lưu  lại điểm đánh giá và nhận xét |

## 1.2 Bác sĩ
**Xem lịch khám**
| ID | Yêu cầu |
|----|---------|
| FR-23 | Hệ thống phải hiển thị danh sách bệnh nhân trong ngày cho bác sĩ |
| FR-24 | Hệ thống phải hiển thị thông tin của bệnh nhân |

**Khám bệnh**
| ID | Yêu cầu |
|----|---------|
| FR-25 | Hệ thống phải cho phép bác sĩ nhập triệu chứng |
| FR-26 | Hệ thống phải yêu cầu bác sĩ bắt buộc nhập chuẩn đoán |

**Kê đơn thuốc**
| ID | Yêu cầu |
|----|---------|
| FR-27 | Hệ thống phải hiển thị danh sách thuốc |
| FR-28 | Hệ thống phải cho phép bác sĩ thêm nhiều thuốc vào đơn |
| FR-29 | Hệ thống phải lưu đơn thuốc vào CSDL |
| FR-30 | Hệ thốg phải cập nhật trạng thái lịch khám là "Completed" |

**Yêu cầu xét nghiệm**
| ID | Yêu cầu |
|----|---------|
| FR-31 | Hệ thống phải cho phép bác sĩ tạo yêu cầu xét nghiệm cho bệnh nhân |
| FR-32 | Hệ thống phải hiển thị danh sách các loại xét nghiệm |
| FR-33 | Hệ thống phải cho phép bác sĩ chọn 1 hay nhiều xét nghiệm |
| FR-34 | Hệ thống phải lưu yêu cầu xẻt nghiệm vào CSDL |
| FR-35 | Hệ thống phải cập nhật trạng thái xét nghiệm là "Pending Result" |

## 1.3 Admin
**Quản lý bác sĩ**
| ID | Yêu cầu |
|----|---------|
| FR-36 | Hệ thống phải cho phép admin thêm bác sĩ |
| FR-37 | Hệ thống phải cho phép admin chỉnh sửa thông tin bác sĩ |
| FR-38 | Hệ thống phải chỉ phép admin xóa bác sĩ khi bác sĩ đang có lịch khám chưa hoàn thành |

**Quản lý chuyên khoa**
| ID | Yêu cầu |
|----|---------|
| FR-39 | Hệ thống phải cho phép admin thêm chuyên khoa |
| FR-40 | Hệ thống phải cho phép admin chỉnh sửa chuyên khoa |
| FR-41 | Hệ thống phải cho phép admin xóa chuyên khoa |

**Quản lý thuốc**
| ID | Yêu cầu |
|----|---------|
| FR-42 | Hệ thống phải cho phép admin thêm thuốc |
| FR-43 | Hệ thống phải cho phép admin chỉnh sửa thuốc |
| FR-44 | Hệ thống phải cho phép admin xóa thuốc |

---
# 2. Phân tích yêu cầu phi chức năng
## 2.1 Hiệu năng
| ID | Yêu cầu | Ghi chú |
|----|---------|---------|
| NFR-01 | Thời gian tải danh sách lịch khám không vượt quá 3 giây | Đo theo thời gian từ khi client gửi request đến khi nhận được response hoàn chỉnh |

## 2.2 Bảo mật
| ID | Yêu cầu | Ghi chú |
|----|---------|---------|
| NFR-02 | Hệ thống phải yêu cầu xác thực người dùng trước khi truy cập chức năng | Nếu truy cập API khi chưa đăng nhập thì phải từ chối (401) |
| NFR-03 | Hệ thống phải phân quyền theo vai trò (Patient, Doctor, Admin) | Nếu truy cập không đúng role API thì 403 |
| NFR-04 | Mật khẩu phải được mã hóa trong CSDL |  |
| NFR-05 | Người dùng của role A chỉ được truy cập và sử dụng API của role A |  |

## 2.3 Tin cậy và sẵn sàng
| ID | Yêu cầu | Ghi chú |
|----|---------|---------|
| NFR-06 | Hệ thống phải sử dụng transaction để đảm bảo tính toàn vẹn dữ liệu | |
| NFR-07 | Hệ thống phải rollback trấnction khi thanh toán thất bại | |
| NFR-08 | Hệ thống phải đảm bảo uptime tối thiểu 99% | |

## 2.4 Tiện dụng
| ID | Yêu cầu | Ghi chú |
|----|---------|---------|
| NFR-09 | Giao diện phải hỗ trợ hiển thị cả trên thiết bị di động và máy tính | |
| NFR- | Các thông báo lỗi phải rõ ràng, dễ hiểu | |

## 2.5 Khả năng bảo trì
| ID | Yêu cầu | Ghi chú |
|----|---------|---------|
| NFR-11 | Hệ thống phải đạt tối thiểu 60% unit test coverage | |

---
# Thiết kế Use Cases
![Use Case Diagram](usecase.svg)

# Thiết kế Wireframe

