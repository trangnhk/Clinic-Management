# Chương 1: Giới thiệu

## 1. Tổng quan đề tài

Clinic Management System là hệ thống quản lý phòng khám được phát triển nhằm hỗ trợ quá trình khám chữa bệnh và quản lý thông tin y tế một cách hiệu quả, giảm thời gian chờ đợi của bệnh nhân và hỗ trợ bác sĩ trong quá trình khám bệnh.

Hệ thống cho phép bệnh nhân đặt lịch khám trực tuyến, thanh toán đặt cọc, xem lịch sử khám bệnh, đơn thuốc và kết quả xét nghiệm. Bác sĩ có thể xem lịch khám, ghi chẩn đoán, kê đơn thuốc và yêu cầu xét nghiệm. Admin quản lý thông tin bác sĩ, chuyên khoa và danh mục thuốc trong hệ thống.

Hệ thống được xây dựng với mục tiêu cải thiện trải nghiệm người dùng, tăng hiệu quả quản lý phòng khám và hỗ trợ lưu trữ dữ liệu y tế một cách chính xác và thuận tiện.

## 2. Mục đích của Test plan

Tài liệu Test Plan này được xây dựng nhằm mô tả kế hoạch kiểm thử cho hệ thống Clinic Management System, bao gồm:

- Phạm vi kiểm thử
- Mục tiêu kiểm thử
- Chiến lược kiểm thử
- Môi trường kiểm thử
- Công cụ kiểm thử
- Tiêu chí bắt đầu và kết thúc kiểm thử
- Các rủi ro và kế hoạch giảm thiểu rủi ro

Tài liệu này đóng vai trò định hướng cho toàn bộ hoạt động kiểm thử nhằm đảm bảo hệ thống hoạt động đúng theo yêu cầu nghiệp vụ và đáp ứng chất lượng trước khi triển khai.

## 3. Mục tiêu của kiểm thử

- Xác minh hệ thống hoạt động đúng theo yêu cầu của đề tài Clinic Management System
- Phát hiện lỗi và các hành vi không đúng trong hệ thống trước khi triển khai.
- Đảm bảo các chức năng chính hoạt động ổn định và chính xác.
- Đảm bảo dữ liệu được xử lý và lưu trữ chính xác.
- Đảm bảo luồng nghiệp vụ giữa bệnh nhân, bác sĩ và admin hoạt động đúng.
- Đánh giá tính ổn định và khả năng sử dụng của hệ thống


## 4. Phạm vi kiểm thử

Tài liệu này tập trung vào kiểm thử chức năng (functional testing) cho hệ thống Clinic Management System, bào gồm:

- Bệnh nhân:
    + Logic đặt lịch khám online (kiểm tra trùng lịch và thời gian hợp lệ)
    + Thanh toán cọc và xác nhận trạng thái giao dịch
    + Xem đơn thuốc và kết quả khám
- Bác sĩ:
    + Xem lịch khám
    + Ghi chẩn đoán bệnh
    + Kê đơn thuốc
- Admin:
    + Các chức năng CRUD đối với bác sĩ, chuyên khoa và thuốc

Ngoài ra, tài liệu này cũng bao gồm:

- Kiểm thử đơn vị (Unit Testing)
- Kiểm thử thủ công (Manual Functional Testing)
- Kiểm thử tích hợp (Integration Testing)
- Kiểm thử hệ thống (System Testing)

Bởi vì những hạn chế về mặt thời gian trong việc phân tích yêu cầu, xây dựng các chức năng của hệ thống v.v.., nhân lực và trình độ chuyên môn của các thành viên nên Automation Testing sẽ không được triển khai trong phạm vi chính của đồ án này.

# Chương 2: Đối tượng kiểm thử và Chức năng được kiểm thử

## 1. Đối tượng kiểm thử

Các thành phần của hệ thống được đưa vào kiểm thử bao gồm:

- Authentication Module: Đăng nhập và xác thực người dùng
- Appointment Module: Chức năng đặt lịch khám và quản lý lịch hẹn
- Payment Module: Thanh toán đặt cọc và các khoản tiền khác
- Prescription Module: Xem và quản lý đơn thuốc
- LabTest Module: Xem và quản lý các loại xét nghiệm và yêu cầu xét nghiệm
- Examination Module: Ghi chẩn đoán và thông tin khám bệnh
- Doctor Module: Quản lý thông tin bác sĩ
- Specialty Module: Quản lý các chuyên khoa
- Patient Module: Quản lý thông tin hồ sơ bệnh nhân
- Medicine Module: Quản lý thông tin bệnh nhân

Các module trên sẽ được kiểm thử thông qua:

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


## 2. Các chức năng được kiểm thử

### 2.1. Chức năng dành cho Bệnh nhân

#### 2.1.1. Đặt lịch khám online

##### 2.1.1.1. Mục tiêu kiểm thử

Kiểm thử chức năng đặt lịch khám trực tuyến của bệnh nhân nhằm đảm bảo hệ thống xử lý chính xác quá trình đặt lịch, kiểm tra lịch trống của bác sĩ và quản lý trạng thái lịch hẹn.

##### 2.1.1.2. Phạm vi kiểm thử

- Xem danh sách chuyên khoa
- Xem danh sách bác sĩ theo chuyên khoa
- Xem thông tin chi tiết bác sĩ
- Xem danh sách khung giờ khám
- Tạo lịch hẹn khám bệnh
- Hủy lịch hẹn


##### 2.1.1.3. Các nhóm trường hợp kiểm thử

- Đặt lịch thành công với dữ liệu hợp lệ
- Kiểm tra dữ liệu bắt buộc khi đặt lịch
- Kiểm tra lịch hẹn với ngày không hợp lệ
- Kiểm tra bác sĩ hoặc lịch khám không tồn tại
- Kiểm tra trạng thái khung giờ khám
- Kiểm tra quyền truy cập theo role
- Kiểm tra xác thực người dùng
- Kiểm tra hủy lịch hẹn hợp lệ và không hợp lệ
- Kiểm tra giải phóng khung giờ sau khi hủy lịch


##### 2.1.1.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử Use Case (Use Case Testing)
- Kiểm thử bảng quyết định (Decision Table Testing)


##### 2.1.1.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


#### 2.1.2. Thanh toán đặt cọc

##### 2.1.2.1. Mục tiêu kiểm thử

Kiểm thử chức năng thanh toán đặt cọc nhằm đảm bảo hệ thống xử lý chính xác giao dịch thanh toán, cập nhật trạng thái lịch hẹn và xử lý tự động các lịch hẹn chưa thanh toán đúng quy định.

##### 2.1.2.2. Phạm vi kiểm thử

- Thanh toán đặt cọc lịch hẹn
- Kiểm tra trạng thái thanh toán
- Kiểm tra tạo bản ghi thanh toán
- Tự động hủy lịch hẹn chưa thanh toán quá thời hạn


##### 2.1.2.3. Các nhóm trường hợp kiểm thử

- Thanh toán thành công với dữ liệu hợp lệ
- Kiểm tra dữ liệu bắt buộc khi thanh toán
- Kiểm tra giá trị thanh toán hợp lệ và không hợp lệ
- Kiểm tra lịch hẹn không tồn tại
- Kiểm tra quyền thanh toán của bệnh nhân
- Kiểm tra trạng thái lịch hẹn trước khi thanh toán
- Kiểm tra thanh toán lặp lại
- Kiểm tra xác thực và phân quyền
- Kiểm tra cơ chế tự động hủy lịch hẹn chưa thanh toán


##### 2.1.2.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử chuyển đổi trạng thái (State Transition Testing)
- Kiểm thử bảng quyết định (Decision Table Testing)


##### 2.1.2.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)


#### 2.1.3. Xem và cập nhật hồ sơ bệnh nhân

##### 2.1.3.1. Mục tiêu kiểm thử

Kiểm thử chức năng quản lý hồ sơ bệnh nhân nhằm đảm bảo người dùng có thể xem, cập nhật và quản lý chính xác thông tin cá nhân và lịch sử lịch hẹn.

##### 2.1.3.2. Phạm vi kiểm thử

- Xem danh sách lịch hẹn cá nhân
- Xem chi tiết lịch hẹn
- Xem hồ sơ cá nhân
- Cập nhật hồ sơ cá nhân


##### 2.1.3.3. Các nhóm trường hợp kiểm thử

- Xem danh sách lịch hẹn theo trạng thái
- Kiểm tra phân trang dữ liệu
- Kiểm tra dữ liệu phân trang không hợp lệ
- Xem chi tiết lịch hẹn hợp lệ và không hợp lệ
- Kiểm tra quyền truy cập dữ liệu
- Cập nhật đầy đủ hoặc từng phần thông tin cá nhân
- Kiểm tra dữ liệu cập nhật không hợp lệ
- Kiểm tra các trường không được phép cập nhật
- Kiểm tra xác thực và phân quyền người dùng


##### 2.1.3.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử Use Case (Use Case Testing)


##### 2.1.3.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)


#### 2.1.4. Đánh giá bác sĩ

##### 2.1.4.1. Mục tiêu kiểm thử

Kiểm thử chức năng đánh giá bác sĩ nhằm đảm bảo bệnh nhân có thể đánh giá sau khi hoàn thành lịch khám và hệ thống tổng hợp đánh giá chính xác.

##### 2.1.4.2. Phạm vi kiểm thử

- Tạo đánh giá bác sĩ
- Xem danh sách đánh giá bác sĩ
- Xem thống kê đánh giá


##### 2.1.4.3. Các nhóm trường hợp kiểm thử

- Tạo đánh giá thành công
- Kiểm tra quyền đánh giá lịch khám
- Kiểm tra lịch hẹn đủ điều kiện đánh giá
- Kiểm tra đánh giá trùng lặp
- Kiểm tra giá trị rating hợp lệ và không hợp lệ
- Kiểm tra dữ liệu bắt buộc
- Kiểm tra tính toán rating trung bình
- Kiểm tra sắp xếp danh sách đánh giá
- Kiểm tra trường hợp bác sĩ chưa có đánh giá


##### 2.1.4.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử Use Case (Use Case Testing)


##### 2.1.4.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


#### 2.1.5. Xem lịch sử khám bệnh

##### 2.1.5.1. Mục tiêu kiểm thử

Kiểm thử chức năng xem lịch sử khám bệnh nhằm đảm bảo hệ thống hiển thị chính xác thông tin khám bệnh, đơn thuốc và thanh toán của bệnh nhân.

##### 2.1.5.2. Phạm vi kiểm thử

- Xem thông tin lịch sử khám bệnh
- Xem kết quả khám bệnh
- Xem đơn thuốc
- Xem thông tin thanh toán


##### 2.1.5.3. Các nhóm trường hợp kiểm thử

- Xem lịch sử khám bệnh thành công
- Kiểm tra lịch hẹn không tồn tại
- Kiểm tra quyền truy cập lịch sử khám bệnh
- Kiểm tra lịch hẹn chưa hoàn thành
- Kiểm tra trường hợp chưa có kết quả khám
- Kiểm tra trường hợp chưa có đơn thuốc
- Kiểm tra trường hợp chưa có thanh toán
- Kiểm tra tính toán tổng chi phí thanh toán
- Kiểm tra trạng thái thanh toán hợp lệ


##### 2.1.5.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Kiểm thử chuyển đổi trạng thái (State Transition Testing)
- Kiểm thử Use Case (Use Case Testing)
- Kiểm thử chức năng (Functional Testing)


##### 2.1.5.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)


### 2.2. Chức năng dành cho Bác sĩ

#### 2.2.1. Quản lý lịch khám

##### 2.2.1.1. Mục tiêu kiểm thử

Kiểm thử chức năng quản lý lịch khám của bác sĩ nhằm đảm bảo hệ thống hiển thị chính xác lịch hẹn, hỗ trợ bác sĩ theo dõi trạng thái khám bệnh và hoàn tất quá trình khám đúng quy trình nghiệp vụ.

##### 2.2.1.2. Phạm vi kiểm thử

- Xem danh sách lịch khám theo ngày
- Lọc lịch khám theo trạng thái
- Xem chi tiết lịch hẹn
- Hoàn tất ca khám


##### 2.2.1.3. Các nhóm trường hợp kiểm thử

- Xem danh sách lịch khám thành công
- Kiểm tra lọc lịch khám theo trạng thái hợp lệ và không hợp lệ
- Kiểm tra dữ liệu đầu vào của tham số ngày
- Kiểm tra dữ liệu phản hồi của lịch khám
- Kiểm tra lịch hẹn không tồn tại
- Kiểm tra quyền truy cập lịch hẹn của bác sĩ
- Kiểm tra xác thực và phân quyền người dùng
- Xem chi tiết lịch hẹn với các trạng thái dữ liệu khác nhau
- Hoàn tất ca khám hợp lệ
- Kiểm tra điều kiện hoàn tất ca khám
- Kiểm tra trạng thái xét nghiệm trước khi hoàn tất khám


##### 2.2.1.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Kiểm thử chuyển đổi trạng thái (State Transition Testing)
- Kiểm thử Use Case (Use Case Testing)


##### 2.2.1.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


#### 2.2.2. Khám bệnh và quản lý hồ sơ khám bệnh

##### 2.2.2.1. Mục tiêu kiểm thử

Kiểm thử chức năng khám bệnh nhằm đảm bảo bác sĩ có thể tạo, cập nhật và lưu kết quả khám bệnh chính xác theo quy trình nghiệp vụ của hệ thống.

##### 2.2.2.2. Phạm vi kiểm thử

- Tạo hồ sơ khám bệnh
- Cập nhật hồ sơ khám bệnh
- Lưu kết quả khám bệnh
- Tạo và cập nhật thông tin thanh toán sau khám


##### 2.2.2.3. Các nhóm trường hợp kiểm thử

- Tạo hồ sơ khám bệnh thành công
- Kiểm tra dữ liệu bắt buộc khi tạo hồ sơ khám bệnh
- Kiểm tra trạng thái lịch hẹn trước khi khám
- Kiểm tra lịch hẹn đã tồn tại hồ sơ khám bệnh
- Kiểm tra quyền truy cập hồ sơ khám bệnh
- Cập nhật hồ sơ khám bệnh hợp lệ và không hợp lệ
- Kiểm tra cập nhật từng phần dữ liệu
- Kiểm tra trạng thái lịch hẹn khi cập nhật hồ sơ
- Lưu kết quả khám bệnh thành công
- Kiểm tra tạo hoặc cập nhật payment record
- Kiểm tra trạng thái hồ sơ khám bệnh trước khi lưu kết quả
- Kiểm tra xác thực và phân quyền người dùng


##### 2.2.2.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Kiểm thử chuyển đổi trạng thái (State Transition Testing)
- Kiểm thử bảng quyết định (Decision Table Testing)
- Kiểm thử Use Case (Use Case Testing)


##### 2.2.2.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


#### 2.2.3. Quản lý đơn thuốc

##### 2.2.3.1. Mục tiêu kiểm thử

Kiểm thử chức năng kê đơn thuốc nhằm đảm bảo bác sĩ có thể quản lý đơn thuốc chính xác trong quá trình khám bệnh.

##### 2.2.3.2. Phạm vi kiểm thử

- Xem danh sách thuốc
- Thêm thuốc vào đơn thuốc
- Xóa thuốc khỏi đơn thuốc


##### 2.2.3.3. Các nhóm trường hợp kiểm thử

- Xem danh sách thuốc thành công
- Thêm thuốc vào đơn thuốc hợp lệ
- Kiểm tra tự động tạo đơn thuốc mới
- Kiểm tra tái sử dụng đơn thuốc đã tồn tại...
- Kiểm tra dữ liệu bắt buộc khi thêm thuốc
- Kiểm tra dữ liệu thuốc không hợp lệ
- Kiểm tra số lượng thuốc hợp lệ và không hợp lệ
- Kiểm tra hồ sơ khám bệnh không tồn tại
- Kiểm tra quyền truy cập của bác sĩ
- Kiểm tra trạng thái lịch hẹn trước khi kê đơn
- Xóa thuốc khỏi đơn thuốc hợp lệ và không hợp lệ
- Kiểm tra chỉnh sửa đơn thuốc sau khi hoàn tất khám
- Kiểm tra xác thực và phân quyền người dùng


##### 2.2.3.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử chuyển đổi trạng thái (State Transition Testing)
- Kiểm thử bảng quyết định (Decision Table Testing)


##### 2.2.3.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


#### 2.2.4. Quản lý xét nghiệm

##### 2.2.4.1. Mục tiêu kiểm thử

Kiểm thử chức năng quản lý yêu cầu xét nghiệm nhằm đảm bảo hệ thống xử lý chính xác việc tạo, theo dõi và quản lý các yêu cầu xét nghiệm trong quá trình khám bệnh.

##### 2.2.4.2. Phạm vi kiểm thử

- Xem danh mục xét nghiệm
- Thêm yêu cầu xét nghiệm
- Xem danh sách yêu cầu xét nghiệm
- Xóa yêu cầu xét nghiệm


##### 2.2.4.3. Các nhóm trường hợp kiểm thử

- Xem danh mục xét nghiệm thành công
- Thêm yêu cầu xét nghiệm hợp lệ
- Kiểm tra yêu cầu xét nghiệm trùng lặp
- Kiểm tra xét nghiệm không tồn tại
- Kiểm tra hồ sơ khám bệnh không tồn tại
- Kiểm tra quyền truy cập của bác sĩ
- Kiểm tra trạng thái lịch hẹn trước khi thêm xét nghiệm
- Xem danh sách xét nghiệm thành công
- Kiểm tra trường hợp chưa có yêu cầu xét nghiệm
- Xóa yêu cầu xét nghiệm hợp lệ và không hợp lệ
- Kiểm tra trạng thái xét nghiệm trước khi xóa
- Kiểm tra xác thực và phân quyền người dùng


##### 2.2.4.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Kiểm thử chuyển đổi trạng thái (State Transition Testing)
- Kiểm thử Use Case (Use Case Testing)


##### 2.2.4.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


#### 2.2.5. Hồ sơ bác sĩ và lịch công tác

##### 2.2.5.1. Mục tiêu kiểm thử

Kiểm thử chức năng quản lý hồ sơ bác sĩ và lịch công tác nhằm đảm bảo hệ thống hiển thị và cập nhật chính xác thông tin cá nhân cũng như lịch làm việc của bác sĩ.

##### 2.2.5.2. Phạm vi kiểm thử

- Xem hồ sơ bác sĩ
- Cập nhật hồ sơ bác sĩ
- Xem lịch công tác theo tháng


##### 2.2.5.3. Các nhóm trường hợp kiểm thử

- Xem hồ sơ bác sĩ thành công
- Cập nhật hồ sơ bác sĩ hợp lệ
- Cập nhật từng phần dữ liệu
- Kiểm tra số năm kinh nghiệm không hợp lệ
- Kiểm tra dữ liệu rỗng khi cập nhật
- Xem lịch công tác theo tháng thành công
- Kiểm tra dữ liệu đầu vào của tháng và năm
- Kiểm tra cấu trúc dữ liệu lịch công tác
- Kiểm tra xác thực và phân quyền người dùng


##### 2.2.5.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử Use Case (Use Case Testing)
- Kiểm thử chức năng (Functional Testing)


##### 2.2.5.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)


### 2.3. Chức năng dành cho Admin

#### 2.3.1. Quản lý bác sĩ

##### 2.3.1.1. Mục tiêu kiểm thử

Kiểm thử chức năng quản lý bác sĩ nhằm đảm bảo quản trị viên có thể quản lý thông tin bác sĩ chính xác và an toàn thông qua hệ thống quản trị.

##### 2.3.1.2. Phạm vi kiểm thử

- Xem danh sách bác sĩ
- Thêm bác sĩ mới
- Cập nhật thông tin bác sĩ
- Xóa bác sĩ
- Tìm kiếm bác sĩ


##### 2.3.1.3. Các nhóm trường hợp kiểm thử

- Hiển thị danh sách bác sĩ thành công
- Thêm mới bác sĩ với dữ liệu hợp lệ
- Kiểm tra các trường dữ liệu bắt buộc
- Kiểm tra định dạng dữ liệu không hợp lệ
- Cập nhật thông tin bác sĩ
- Xóa bác sĩ hợp lệ và không hợp lệ
- Tìm kiếm bác sĩ theo thông tin
- Kiểm tra phân quyền truy cập quản trị viên


##### 2.3.1.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử CRUD
- Kiểm thử chức năng (Functional Testing)


##### 2.3.1.5. Loại kiểm thử

- Unit Testing (kiểm thử đơn vị)
- Manual Testing (kiểm thử thủ công)


#### 2.3.2. Quản lý chuyên khoa

##### 2.3.2.1. Mục tiêu kiểm thử

Kiểm thử chức năng quản lý chuyên khoa nhằm đảm bảo hệ thống quản lý chính xác danh mục chuyên khoa phục vụ cho quá trình đặt lịch và khám bệnh.

##### 2.3.2.2. Phạm vi kiểm thử

- Xem danh sách chuyên khoa
- Thêm chuyên khoa
- Cập nhật chuyên khoa
- Xóa chuyên khoa


##### 2.3.2.3. Các nhóm trường hợp kiểm thử

- Hiển thị danh sách chuyên khoa thành công
- Thêm mới chuyên khoa hợp lệ
- Kiểm tra dữ liệu chuyên khoa không hợp lệ
- Cập nhật thông tin chuyên khoa
- Xóa chuyên khoa hợp lệ và không hợp lệ
- Kiểm tra trùng tên chuyên khoa
- Kiểm tra quyền truy cập của quản trị viên


##### 2.3.2.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Kiểm thử CRUD
- Kiểm thử chức năng (Functional Testing)


##### 2.3.2.5. Loại kiểm thử

- Manual Testing (kiểm thử thủ công)


#### 2.3.3. Quản lý thuốc

##### 2.3.3.1. Mục tiêu kiểm thử

Kiểm thử chức năng quản lý thuốc nhằm đảm bảo quản trị viên có thể quản lý chính xác danh mục thuốc phục vụ cho hoạt động kê đơn trong hệ thống.

##### 2.3.3.2. Phạm vi kiểm thử

- Xem danh sách thuốc
- Thêm thuốc mới
- Cập nhật thông tin thuốc
- Xóa thuốc
- Tìm kiếm thuốc


##### 2.3.3.3. Các nhóm trường hợp kiểm thử

- Hiển thị danh sách thuốc thành công
- Thêm thuốc mới với dữ liệu hợp lệ
- Kiểm tra dữ liệu thuốc không hợp lệ
- Kiểm tra dữ liệu bắt buộc
- Cập nhật thông tin thuốc
- Xóa thuốc hợp lệ và không hợp lệ
- Kiểm tra quyền truy cập quản trị viên


##### 2.3.3.4. Kỹ thuật kiểm thử áp dụng

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử CRUD
- Kiểm thử chức năng (Functional Testing)


##### 2.3.3.5. Loại kiểm thử

- Manual Testing (kiểm thử thủ công)


#### 2.3.4. Chức năng dành cho quản trị viên

Các chức năng quản trị được triển khai thông qua framework Flask-Admin nhằm hỗ trợ quản lý dữ liệu hệ thống theo mô hình CRUD (Create, Read, Update, Delete). Do phần lớn chức năng quản trị được framework hỗ trợ sẵn, hoạt động kiểm thử tập trung chủ yếu vào:

- Kiểm tra tính đúng đắn của dữ liệu
- Kiểm tra validation dữ liệu đầu vào
- Kiểm tra phân quyền truy cập
- Kiểm tra thao tác CRUD trên dữ liệu hệ thống


# Chương 3: Chiến lược kiểm thử

## 1. Định hướng kiểm thử

Chiến lược kiểm thử của hệ thống quản lý phòng khám được xây dựng theo hướng kết hợp giữa kiểm thử đơn vị (Unit Testing) và kiểm thử thủ công (Manual Functional Testing) nhằm đảm bảo chất lượng phần mềm một cách toàn diện.

Hoạt động kiểm thử tập trung vào:

- Xác minh tính đúng đắn của các chức năng theo yêu cầu nghiệp vụ
- Kiểm tra luồng xử lý chính của hệ thống giữa các vai trò:
● Bệnh nhân
● Bác sĩ
● Quản trị viên
- Đảm bảo dữ liệu được xử lý và hiển thị chính xác giữa các phân hệ
- Kiểm tra cơ chế xác thực và phân quyền người dùng
- Kiểm tra trạng thái xử lý của lịch hẹn, khám bệnh, thanh toán và xét nghiệm

Hệ thống được kiểm thử dựa trên các luồng nghiệp vụ chính:

- Đặt lịch khám trực tuyến
- Thanh toán đặt cọc
- Khám bệnh và lưu kết quả khám
- Kê đơn thuốc
- Quản lý xét nghiệm
- Xem lịch sử khám bệnh
- Đánh giá bác sĩ
- Quản lý dữ liệu hệ thống của quản trị viên

Các hoạt động kiểm thử chủ yếu áp dụng phương pháp kiểm thử hộp đen (Black-box Testing) kết hợp với các kỹ thuật:

- Phân vùng tương đương (Equivalence Partitioning – EP)
- Phân tích giá trị biên (Boundary Value Analysis – BVA)
- Kiểm thử Use Case (Use Case Testing)
- Kiểm thử bảng quyết định (Decision Table Testing)
- Kiểm thử chuyển đổi trạng thái (State Transition Testing)
- Kiểm thử chức năng (Functional Testing)


## 2. Định hướng kiểm thử (Unit Testing)

Kiểm thử đơn vị được thực hiện nhằm kiểm tra tính đúng đắn của từng thành phần riêng lẻ trước khi tích hợp vào hệ thống. Hoạt động kiểm thử tập trung chủ yếu vào:

- API endpoints
- Business logic
- Validation logic
- Role authorization
- Appointment workflow
- Payment processing
- Examination workflow
- Prescription management
- Lab test processing

Các module được kiểm thử bao gồm:

- Authentication Module: Đăng nhập và xác thực người dùng
- Appointment Module: Đặt lịch, hủy lịch, kiểm tra trạng thái lịch hẹn
- Medical History Module: Xem lịch sử khám bệnh
- Payment Module: Thanh toán đặt cọc và xử lý auto-cancel
- Prescription Module: Xem và quản lý đơn thuốc
- LabTest Module: Xem và quản lý các loại xét nghiệm và yêu cầu xét nghiệm
- Examination Module: Tạo và cập nhật kết quả khám h
- Doctor Module: Quản lý thông tin bác sĩ
- Specialty Module: Quản lý các chuyên khoa
- Patient Module: Quản lý thông tin hồ sơ bệnh nhân
- Medicine Module: Quản lý thông tin bệnh nhân
- Review Module: Đánh giá bác sĩ

Các trường hợp kiểm thử được thiết kế bao phủ:

- Trường hợp hợp lệ (Normal Case)
- Trường hợp không hợp lệ (Negative Case)
- Trường hợp biên (Boundary Case)
- Trường hợp kiểm tra trạng thái hệ thống (State Validation)
- Trường hợp kiểm tra phân quyền (Authorization Testing)

Kết quả kiểm thử được đánh giá dựa trên:

- Tính đúng đắn của kết quả xử lý
- Tính ổn định của luồng nghiệp vụ
- Độ bao phủ mã nguồn (Code Coverage)

Mục tiêu độ bao phủ mã nguồn:

- Line Coverage ≥ 70%
- Function Coverage ≥ 70%


## 3. Kiểm thử thủ công (Manual Functional Testing)

Kiểm thử thủ công được thực hiện nhằm đánh giá tính đầy đủ của chức năng hệ thống và khả năng xử lý các tình huống thực tế theo góc nhìn người dùng. Hoạt động kiểm thử tập trung vào:

- Luồng nghiệp vụ chính của bệnh nhân
- Luồng khám bệnh của bác sĩ
- Chức năng quản trị hệ thống
- Giao diện và trải nghiệm người dùng
- Kiểm tra dữ liệu hiển thị giữa các phân hệ

Các kịch bản kiểm thử được xây dựng dựa trên:

- Yêu cầu hệ thống
- Use Case nghiệp vụ
- Luồng xử lý thực tế của hệ thống

Các chức năng được thực hiện kiểm thử thủ công bao gồm:

- Đặt lịch khám
- Thanh toán đặt cọc
- Xem lịch khám
- Khám bệnh
- Kê đơn thuốc
- Quản lý xét nghiệm
- Quản lý bác sĩ
- Quản lý thuốc
- Quản lý chuyên khoa

Các test case thủ công được quản lý thông qua Google Sheets và được theo dõi theo trạng thái:

- Passed
- Failed
- Blocked


## 4. Kiểm thử tích hợp (Integration Testing)

Kiểm thử tích hợp được thực hiện nhằm đảm bảo các phân hệ trong hệ thống hoạt động chính xác khi tương tác với nhau và dữ liệu được đồng bộ xuyên suốt giữa các vai trò người dùng.

Hoạt động kiểm thử tích hợp tập trung vào các luồng nghiệp vụ chính của hệ thống, bao gồm:

- Bệnh nhân đặt lịch khám và thanh toán đặt cọc
- Bác sĩ tiếp nhận lịch khám và thực hiện khám bệnh
- Bác sĩ kê đơn thuốc và lưu kết quả khám
- Bệnh nhân xem kết quả khám và đơn thuốc
- Quản lý trạng thái lịch hẹn và khung giờ khám
- Đồng bộ dữ liệu giữa bệnh nhân, bác sĩ và hệ thống quản trị

Kiểm thử tích hợp được thực hiện dưới hình thức Manual End-to-End Testing (E2E Testing), trong đó toàn bộ luồng nghiệp vụ được kiểm tra xuyên suốt từ đầu đến cuối theo các tình huống sử dụng thực tế của người dùng.

Các kịch bản kiểm thử tích hợp bao gồm:

- Luồng đặt lịch → thanh toán → khám bệnh → kê đơn → xem kết quả
- Thanh toán thất bại và xử lý trạng thái lịch hẹn
- Kiểm tra đồng bộ lịch khám giữa bệnh nhân và bác sĩ
- Kiểm tra hiển thị kết quả khám sau khi hoàn tất khám bệnh
- Kiểm tra xử lý khi dữ liệu khám chưa hoàn tất
- Kiểm tra nhiều bệnh nhân đặt cùng một khung giờ
- Kiểm tra khả năng lưu trạng thái dữ liệu khi refresh hệ thống

Các hoạt động kiểm thử được thực hiện thông qua:

- Manual Functional Testing trên giao diện hệ thống
- API Testing bằng Postman
- Kiểm tra dữ liệu phản hồi giữa các module
- Đối chiếu trạng thái dữ liệu trong hệ thống

Các nội dung kiểm thử bao gồm:

- Truyền dữ liệu giữa các module
- Đồng bộ trạng thái hệ thống
- Tính toàn vẹn dữ liệu
- Xử lý lỗi giữa các phân hệ
- Kiểm tra luồng nghiệp vụ xuyên suốt giữa các vai trò người dùng


## 5. Kiểm thử hệ thống (System Testing)

Kiểm thử hệ thống được thực hiện nhằm đánh giá toàn bộ hệ thống quản lý phòng khám sau khi các phân hệ đã được tích hợp hoàn chỉnh. Hoạt động kiểm thử tập trung vào:

- Tính đúng đắn của chức năng hệ thống
- Luồng nghiệp vụ tổng thể
- Tính ổn định của hệ thống
- Tính nhất quán dữ liệu giữa các phân hệ
- Khả năng xử lý lỗi và ngoại lệ
- Cơ chế xác thực và phân quyền người dùng

Việc kiểm thử được thực hiện dựa trên các tình huống sử dụng thực tế của:
● Bệnh nhân
● Bác sĩ
● Quản trị viên

Các kịch bản kiểm thử hệ thống được thực hiện dưới hình thức Manual End-to-End Testing nhằm mô phỏng toàn bộ quy trình sử dụng hệ thống từ đầu đến cuối. Các luồng nghiệp vụ được kiểm thử bao gồm:

- Đặt lịch khám và thanh toán đặt cọc
- Khám bệnh và lưu kết quả khám
- Kê đơn thuốc và xét nghiệm
- Xem lịch sử khám bệnh
- Đánh giá bác sĩ
- Quản lý dữ liệu hệ thống của quản trị viên

Thông qua các hoạt động kiểm thử này, hệ thống được đánh giá như một sản phẩm hoàn chỉnh nhằm đảm bảo đáp ứng đúng yêu cầu nghiệp vụ và nhu cầu sử dụng thực tế.

## 6. Phạm vi kiểm thử không thực hiện

Trong phạm vi hiện tại của đồ án, các loại kiểm thử sau chưa được triển khai:

- Automation Testing
- Performance Testing
- Load Testing
- Stress Testing
- Security Penetration Testing
- Cross-browser Automation Testing
- Continuous Integration Testing

Nguyên nhân là do phạm vi đồ án tập trung chủ yếu vào:

- Xây dựng chức năng hệ thống
- Unit Testing
- Manual Functional Testing
- Kiểm thử nghiệp vụ chính của hệ thống

Automation Testing được xem là hướng phát triển mở rộng trong tương lai nhằm hỗ trợ:

- Regression Testing
- Continuous Testing
- Automated UI Testing


# Chương 4: Môi trường kiểm thử

## 1. Phần cứng

| Thành phần | Cấu hình |
| :-- | :-- |
| CPU | Intel Core i5 hoặc tương đương |
| RAM | 8GB trở lên |
| Storage | SSD 256GB trở lên |
| Thiết bị kiểm thử | Máy tính cá nhân hoặc thiết bị tương đương |

## 2. Phần mềm

| Thành phần | Mô tả |
| :-- | :-- |
| Hệ điều hành | Windows 10/11 hoặc macOS |
| Trình duyệt kiểm thử | Google Chrome, Microsoft Edge |
| Backend Framework | Flask |
| Database | MySQL |
| API Testing Tool | Postman |
| Admin Framework | Flask-Admin |

## 3. Dữ liệu kiểm thử

Dữ liệu kiểm thử được chuẩn bị nhằm phục vụ cho các luồng nghiệp vụ chính của hệ thống. Các nhóm dữ liệu kiểm thử bao gồm:

- Tài khoản bệnh nhân
- Tài khoản bác sĩ
- Tài khoản quản trị viên
- Danh mục chuyên khoa
- Danh mục thuốc
- Danh mục xét nghiệm
- Dữ liệu lịch khám
- Dữ liệu thanh toán
- Dữ liệu đơn thuốc
- Dữ liệu đánh giá bác sĩ

Ngoài dữ liệu hợp lệ, hệ thống cũng sử dụng các dữ liệu không hợp lệ nhằm kiểm tra:

- Validation dữ liệu đầu vào
- Boundary cases
- Authorization
- Error handling


## 4. Công cụ hỗ trợ kiểm thử

| Công cụ | Mục đích sử dụng |
| :-- | :-- |
| Pytest | Thực hiện Unit Testing |
| Postman | Kiểm thử API |
| Google Chrome DevTools | Debug giao diện và kiểm tra dữ liệu |
| Google Sheets | Quản lý test case và bug list |

# Chương 5: Điều kiện và kế hoạch kiểm thử

## 1. Điều kiện bắt đầu kiểm thử (Entry Criteria)

Hoạt động kiểm thử được bắt đầu khi đáp ứng các điều kiện sau:

- Các chức năng chính của hệ thống đã được triển khai
- Yêu cầu hệ thống đã được xác định
- Database và dữ liệu kiểm thử đã được chuẩn bị
- Môi trường kiểm thử đã sẵn sàng
- Các test case đã được xây dựng
- API và giao diện người dùng có thể truy cập được

Đối với Unit Testing:

- Source code phải biên dịch và chạy thành công
- Các dependency cần thiết đã được cài đặt đầy đủ

Đối với Manual Testing và E2E Testing:

- Các module liên quan phải được tích hợp hoàn chỉnh
- Dữ liệu kiểm thử phải được khởi tạo trước khi thực hiện kiểm thử


## 2. Điều kiện kết thúc kiểm thử (Exit Criteria)

Quá trình kiểm thử được xem là hoàn tất khi:

- Tất cả test case đã được thực thi
- Kết quả kiểm thử đã được ghi nhận đầy đủ
- Các lỗi nghiêm trọng (Critical/High) đã được xử lý hoặc ghi nhận
- Các luồng nghiệp vụ chính hoạt động ổn định
- Không còn lỗi gây ảnh hưởng nghiêm trọng đến chức năng chính của hệ thống

Ngoài ra:

- Kết quả Unit Testing đạt yêu cầu
- Các kịch bản Integration Testing và E2E Testing hoạt động đúng theo mong đợi
- Dữ liệu giữa các module được đồng bộ chính xác


## 3. Kế hoạch thực hiện

Hoạt động kiểm thử được thực hiện theo các giai đoạn sau:

1. Test Planning: Xây dựng Test plan
2. Test Design: Thiết kế Test Case
3. Unit Testing: Kiểm thử từng module chức năng
4. Integration Testing: Kiểm thử luồng liên kết giữa các module
5. System Testing: Kiểm thử toàn bộ hệ thống
6. Defect Reporting: Ghi nhận và theo dõi lỗi
7. Test Reporting: Tổng hợp và báo cáo kết quả kiểm thử

## 4. Tiêu chí đánh giá kết quả kiểm thử

Kết quả kiểm thử được đánh giá dựa trên:

- Tỷ lệ test case passed
- Số lượng lỗi phát hiện
- Mức độ nghiêm trọng của lỗi
- Độ ổn định của các luồng nghiệp vụ
- Tính chính xác của dữ liệu hệ thống

Ngoài ra, hệ thống được đánh giá dựa trên khả năng:

- Xử lý đúng nghiệp vụ
- Đồng bộ dữ liệu giữa các module
- Kiểm soát quyền truy cập người dùng
- Xử lý lỗi và ngoại lệ

