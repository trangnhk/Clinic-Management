# Doctor API Documentation

> **Clinic Management System** – Doctor API Reference

---

## Overview

Tài liệu này mô tả toàn bộ Doctor API cho hệ thống **Clinic Management System**.

| Thông tin | Chi tiết |
|:--|:--|
| **Base URL** | `/api/doctors` |
| **Authentication** | JWT Bearer Token |
| **Role Required** | `DOCTOR` |

### Authentication Header

```http
Authorization: Bearer <access_token>
```

---

## Table of Contents

- [Doctor Profile APIs](#doctor-profile-apis)
  - [GET /profile](#1-get-doctor-profile)
  - [PATCH /profile](#2-update-doctor-profile)
  - [GET /profile/calendar](#3-get-doctor-calendar)
- [Appointment APIs](#appointment-apis)
  - [GET /appointments](#4-get-appointments-in-day)
  - [GET /appointments/{id}](#5-get-appointment-detail)
- [Examination APIs](#examination-apis)
  - [POST /examinations](#6-create-examination)
  - [PATCH /examinations/{id}](#7-update-examination)
- [Prescription APIs](#prescription-apis)
  - [POST /examinations/{id}/prescriptions](#8-add-prescription-detail)
  - [DELETE /prescriptions/{detail_id}](#9-delete-prescription-detail)
- [Lab Test APIs](#lab-test-apis)
  - [POST /examinations/{id}/lab-tests](#10-add-lab-test-request)
  - [GET /examinations/{id}/lab-tests](#11-get-lab-tests)
  - [DELETE /lab-tests/{id}](#12-delete-lab-test-request)
- [Save & Complete APIs](#save--complete-apis)
  - [POST /examinations/{id}/save](#13-save-examination)
  - [POST /appointments/{id}/complete](#14-complete-appointment)
- [Medicine APIs](#medicine-apis)
  - [GET /medicines](#15-get-medicines)
- [Lab Test Catalog APIs](#lab-test-catalog-apis)
  - [GET /tests](#16-get-all-lab-tests)
- [Common Error Responses](#common-error-responses)

---

## Doctor Profile APIs

### 1. Get Doctor Profile

Lấy thông tin hồ sơ bác sĩ hiện tại.

**Headers**

| Key | Value |
|:--|:--|
| `Authorization` | `Bearer JWT_TOKEN` |

**Response `200 OK`**

```json
{
  "doctor_id": "DR000000001",
  "fullname": "BS. Nguyễn Minh Khoa",
  "phone_number": "0901234567",
  "date_of_birth": "1985-06-15",
  "address": "123 Lê Lợi, Q.1, TP.HCM",
  "specialization": "Cardiology",
  "specialization_id": 1,
  "experience_years": 10,
  "description": "Bác sĩ có nhiều năm kinh nghiệm",
  "rating": 4.5,
  "avatar": "https://example.com/avatar.png"
}
```

**Response `403 Forbidden`**

```json
{
  "error": "Forbidden"
}
```

---

### 2. Update Doctor Profile

Cập nhật hồ sơ bác sĩ.

**Headers**

| Key | Value |
|:--|:--|
| `Authorization` | `Bearer JWT_TOKEN` |

**Request Body**

```json
{
  "fullname": "BS. Nguyễn Minh Khoa",
  "phone_number": "0901234567",
  "experience_years": 10,
  "description": "Bác sĩ chuyên khoa tim mạch"
}
```

**Validation Rules**

| Field | Rule |
|:--|:--|
| `phone_number` | Phải đúng 10 chữ số |
| `experience_years` | >= 0 |

**Response `200 OK`**

```json
{
  "doctor_id": "DR000000001",
  "fullname": "BS. Nguyễn Minh Khoa",
  "phone_number": "0901234567",
  "experience_years": 10,
  "description": "Bác sĩ chuyên khoa tim mạch",
  "specialization": "Cardiology",
  "rating": 4.5,
  "avatar": "https://example.com/avatar.png"
}
```

---

### 3. Get Doctor Calendar

Lấy lịch khám theo tháng.

**Query Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `month` | `integer` | v | Tháng (1–12) |
| `year` | `integer` | v | Năm (2026–2100) |

**Example Request**

```http
GET /profile/calendar?month=4&year=2026
```

**Response `200 OK`**

```json
{
  "month": 4,
  "year": 2026,
  "days_with_appointments":,[1][2][3][4]
  "calendar": {
    "1": [
      {
        "appointment_id": 10,
        "status": "WAITING_EXAMINATION",
        "start_time": "08:00"
      }
    ]
  }
}
```

---

## Appointment APIs

### 4. Get Appointments In Day

Lấy danh sách lịch khám trong ngày.

**Query Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `date` | `string` | v | Format `YYYY-MM-DD` |
| `status` | `string` | x | Lọc theo trạng thái |

**Allowed `status` Values**

| Value | Mô tả |
|:--|:--|
| `WAITING_EXAMINATION` | Chờ khám |
| `IN_PROGRESS` | Đang khám |
| `PENDING_RESULT` | Chờ kết quả xét nghiệm |
| `COMPLETED` | Đã hoàn thành |

**Example Request**

```http
GET /appointments?date=2026-04-15
```

**Response `200 OK`**

```json
[
  {
    "appointment_id": 10,
    "date": "2026-04-15",
    "status": "WAITING_EXAMINATION",
    "start_time": "08:00",
    "end_time": "08:30",
    "can_examine": true,
    "can_complete": false,
    "patient": {
      "id": 1,
      "name": "Nguyễn Văn An",
      "email": "patient@mail.com",
      "date_of_birth": "1990-01-01",
      "address": "TP.HCM"
    }
  }
]
```

---

### 5. Get Appointment Detail

Lấy chi tiết lịch khám.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Appointment ID |

**Response `200 OK`**

```json
{
  "appointment_id": 10,
  "date": "2026-04-15",
  "status": "IN_PROGRESS",
  "symptoms": "Đau đầu, sốt nhẹ",
  "patient": {
    "id": 1,
    "patient_code": "BN000000001",
    "fullname": "Nguyễn Văn An",
    "phone_number": "0901234567",
    "email": "patient@mail.com",
    "date_of_birth": "1990-01-01",
    "address": "TP.HCM"
  },
  "examination": {
    "id": 5,
    "created_date": "2026-04-15",
    "diagnosis": "Viêm họng"
  }
}
```

---

## Examination APIs

### 6. Create Examination

Tạo phiếu khám bệnh.

**Request Body**

```json
{
  "appointment_id": 10,
  "diagnosis": "Viêm họng cấp",
  "symptoms": "Đau họng, sốt 38 độ"
}
```

**Response `201 Created`**

```json
{
  "id": 5,
  "appointment_id": 10,
  "created_date": "2026-04-15",
  "diagnosis": "Viêm họng cấp",
  "symptoms": "Đau họng, sốt 38 độ"
}
```

---

### 7. Update Examination

Cập nhật phiếu khám.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Examination ID |

**Request Body**

```json
{
  "diagnosis": "Viêm họng mãn tính",
  "symptoms": "Đau họng kéo dài"
}
```

**Response `200 OK`**

```json
{
  "id": 5,
  "diagnosis": "Viêm họng mãn tính",
  "symptoms": "Đau họng kéo dài"
}
```

---

## Prescription APIs

### 8. Add Prescription Detail

Thêm thuốc vào đơn thuốc.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Examination ID |

**Request Body**

```json
{
  "medicine_id": 3,
  "quantity": 10,
  "dosage": "2 lần/ngày",
  "instruction": "Uống sau ăn"
}
```

**Response `201 Created`**

```json
{
  "prescription_id": 3,
  "detail_id": 8,
  "medicine_id": 3,
  "quantity": 10,
  "dosage": "2 lần/ngày",
  "instruction": "Uống sau ăn"
}
```

---

### 9. Delete Prescription Detail

Xóa thuốc khỏi đơn thuốc.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `detail_id` | `integer` | Prescription Detail ID |

**Response `200 OK`**

```json
{
  "message": "Deleted successfully"
}
```

---

## Lab Test APIs

### 10. Add Lab Test Request

Tạo yêu cầu xét nghiệm.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Examination ID |

**Request Body**

```json
{
  "test_id": 2
}
```

**Response `201 Created`**

```json
{
  "id": 5,
  "test_id": 2,
  "appointment_id": 10,
  "status": "PENDING"
}
```

---

### 11. Get Lab Tests

Lấy danh sách xét nghiệm của phiếu khám.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Examination ID |

**Response `200 OK`**

```json
[
  {
    "id": 5,
    "test_id": 2,
    "test_name": "Xét nghiệm máu",
    "test_price": 150000,
    "status": "PENDING",
    "result": "Các chỉ số bình thường"
  }
]
```

---

### 12. Delete Lab Test Request

Xóa yêu cầu xét nghiệm.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Lab Test Request ID |

**Response `200 OK`**

```json
{
  "message": "Deleted"
}
```

---

## Save & Complete APIs

### 13. Save Examination

Lưu phiếu khám và cập nhật thông tin Payment.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Examination ID |

**Response `200 OK`**

```json
{
  "medicine": 150000,
  "lab_test": 100000
}
```

---

### 14. Complete Appointment

Hoàn thành lịch khám.

**Path Parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| `id` | `integer` | Appointment ID |

**Response `200 OK`**

```json
{
  "appointment_id": 10,
  "status": "COMPLETED",
  "message": "Appointment completed successfully"
}
```

---

## Medicine APIs

### 15. Get Medicines

Lấy danh sách thuốc trong hệ thống.

**Response `200 OK`**

```json
[
  {
    "id": 1,
    "name": "Paracetamol",
    "unit": "Viên",
    "price": 5000,
    "stock_quantity": 100
  }
]
```

---

## Lab Test Catalog APIs

### 16. Get All Lab Tests

Lấy danh mục xét nghiệm.

**Response `200 OK`**

```json
[
  {
    "id": 1,
    "name": "Xét nghiệm máu",
    "price": 150000,
    "description": "Kiểm tra các chỉ số máu cơ bản"
  }
]
```

---

## Common Error Responses

| Status Code | Ý nghĩa | Response Body |
|:--:|:--|:--|
| `400` | Bad Request – Dữ liệu không hợp lệ | `{ "error": "Invalid request" }` |
| `401` | Unauthorized – Thiếu hoặc sai token | `{ "error": "Unauthorized" }` |
| `403` | Forbidden – Không đủ quyền truy cập | `{ "error": "Forbidden" }` |
| `404` | Not Found – Không tìm thấy tài nguyên | `{ "error": "Doctor not found" }` |
| `500` | Internal Server Error | `{ "error": "Internal server error" }` |

---

> **Lưu ý:** Tất cả các endpoint đều yêu cầu role `DOCTOR`.  
> Truy cập bằng role khác sẽ nhận phản hồi `403 Forbidden`.