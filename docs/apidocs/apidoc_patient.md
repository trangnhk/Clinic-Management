# Patient API Documentation

> **Clinic Management System** – Patient API Reference

---

## Overview

| Thông tin | Chi tiết |
|:--|:--|
| **Base URL** | `/api/patient` |
| **Authentication** | JWT Bearer Token _(một số endpoint yêu cầu)_ |
| **Role Required** | `PATIENT` |

### Authentication Header

```http
Authorization: Bearer <access_token>
```

---

## Table of Contents

- [Booking Appointment Flow](#1-booking-appointment-flow)
  - [GET /specializations](#11-get-all-specializations)
  - [GET /doctors](#12-get-doctors)
  - [GET /doctors/{id}](#13-get-doctor-detail)
  - [GET /timeslots](#14-get-available-timeslots)
  - [POST /appointments](#15-book-appointment)
  - [POST /payments](#16-make-payment)
- [Appointment Management](#2-appointment-management)
  - [GET /appointments](#21-get-patient-appointments)
  - [GET /appointments/{id}](#22-get-appointment-detail)
  - [PATCH /appointments/{id}/cancel](#23-cancel-appointment)
- [Profile Management](#3-profile-management)
  - [GET /profile](#31-get-patient-profile)
  - [PATCH /profile](#32-update-patient-profile)
- [Medical History](#4-medical-history)
  - [GET /appointments/{id}/medical-history](#41-get-medical-history)
  - [POST /appointments/{id}/review](#42-create-review)
  - [GET /doctors/{id}/reviews](#43-get-doctor-reviews)
- [Common Error Responses](#common-error-responses)

---

## 1. Booking Appointment Flow

### 1.1. Get All Specializations

Lấy danh sách tất cả chuyên khoa trong hệ thống.

> 🔓 **Không yêu cầu xác thực**

**Response `200 OK`**

```json
[
  {
    "id": 1,
    "name": "Cardiology"
  },
  {
    "id": 2,
    "name": "Neurology"
  }
]
```

---

### 1.2. Get Doctors

Lấy danh sách bác sĩ, có thể lọc theo chuyên khoa.

> 🔓 **Không yêu cầu xác thực**

**Query Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `specialization_id` | `integer` | x | ID chuyên khoa |

**Example Request**

```http
GET /doctors?specialization_id=1
```

**Response `200 OK`**

```json
[
  {
    "id": 2,
    "name": "BS. Nguyễn Minh Khoa",
    "specialization": "Cardiology",
    "avatar": "https://example.com/avatar.png",
    "rating": 5
  }
]
```

**Response `400 Bad Request`**

```json
{
  "error": "Invalid specialization_id"
}
```

---

### 1.3. Get Doctor Detail

Lấy thông tin chi tiết bác sĩ.

> 🔓 **Không yêu cầu xác thực**

**Path Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `id` | `integer` | v | ID bác sĩ |

**Response `200 OK`**

```json
{
  "id": 2,
  "name": "BS. Nguyễn Minh Khoa",
  "specialization": "Cardiology",
  "avatar": "https://example.com/avatar.png",
  "rating": 4.5,
  "introduce": "Bác sĩ có 10 năm kinh nghiệm",
  "total_reviews": 12
}
```

**Response `404 Not Found`**

```json
{
  "error": "Doctor not found"
}
```

---

### 1.4. Get Available Timeslots

Lấy danh sách lịch trống của bác sĩ theo ngày.

> 🔓 **Không yêu cầu xác thực**

**Query Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `doctor_id` | `integer` | v | ID bác sĩ |
| `date` | `string` | v | Ngày khám (`YYYY-MM-DD`) |

**Example Request**

```http
GET /timeslots?doctor_id=2&date=2026-04-15
```

**Response `200 OK`**

```json
[
  {
    "schedule_id": 5,
    "start_time": "08:00",
    "end_time": "09:00",
    "available": true
  }
]
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "doctor_id must be integer" }` |
| `400` | `{ "error": "Missing parameters" }` |
| `400` | `{ "error": "Invalid date format" }` |

---

### 1.5. Book Appointment

Đặt lịch khám với bác sĩ.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Request Body**

```json
{
  "doctor_id": 2,
  "schedule_id": 5,
  "date": "2026-04-15",
  "notes": "Đau đầu"
}
```

**Request Body Fields**

| Field | Type | Required | Description |
|:--|:--|:--:|:--|
| `doctor_id` | `integer` | v | ID bác sĩ |
| `schedule_id` | `integer` | v | ID lịch khám |
| `date` | `string` | v | Ngày khám (`YYYY-MM-DD`) |
| `notes` | `string` | x | Triệu chứng ban đầu |

**Response `200 OK`**

```json
{
  "id": 10,
  "patient_name": "Nguyen Van A",
  "doctor_name": "Dr. Strange",
  "date": "2026-04-15",
  "status": "PENDING_PAYMENT",
  "payment": "PENDING"
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Missing required fields" }` |
| `403` | `{ "error": "Forbidden" }` |
| `404` | `{ "error": "Patient not found" }` |

---

### 1.6. Make Payment

Thanh toán đặt cọc cho lịch khám.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Request Body**

```json
{
  "appointment_id": 10,
  "amount": 150.0
}
```

**Response `200 OK`**

```json
{
  "payment_id": 5,
  "status": "PAID",
  "amount": 150.0,
  "payment_type": "DEPOSIT"
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Missing required fields" }` |
| `403` | `{ "error": "Forbidden" }` |

---

## 2. Appointment Management

### 2.1. Get Patient Appointments

Lấy danh sách lịch khám của bệnh nhân.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Query Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `status` | `string` | x | Lọc theo trạng thái |

**Allowed `status` Values**

| Value | Mô tả |
|:--|:--|
| `WAITING_EXAMINATION` | Chờ khám |
| `PENDING_PAYMENT` | Chờ thanh toán |
| `PENDING_RESULT` | Chờ kết quả xét nghiệm |
| `COMPLETED` | Đã hoàn thành |
| `CANCELED` | Đã huỷ |

**Response `200 OK`**

```json
[
  {
    "id": 2,
    "date": "2026-04-15",
    "status": "COMPLETED"
  }
]
```

**Response `400 Bad Request`**

```json
{
  "error": "Invalid status"
}
```

---

### 2.2. Get Appointment Detail

Xem chi tiết lịch khám.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Path Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `id` | `integer` | v | ID lịch khám |

**Response `200 OK`**

```json
{
  "id": 10,
  "patient_name": "Nguyen Van A",
  "doctor_name": "Dr. B",
  "date": "2026-04-15",
  "status": "BOOKED",
  "notes": "Đau đầu"
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `403` | `{ "error": "Forbidden" }` |
| `404` | `{ "error": "Appointment not found" }` |

---

### 2.3. Cancel Appointment

Huỷ lịch khám.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Path Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `id` | `integer` | v | ID lịch khám |

**Response `200 OK`**

```json
{
  "message": "Canceled successfully"
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Can not cancel appointment" }` |
| `403` | `{ "error": "Forbidden" }` |

---

## 3. Profile Management

### 3.1. Get Patient Profile

Lấy thông tin bệnh nhân và lịch sử khám bệnh (có phân trang).

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Query Parameters**

| Parameter | Type | Required | Default |
|:--|:--|:--:|:--:|
| `page` | `integer` | x | `1` |
| `per_page` | `integer` | x | `10` |

**Response `200 OK`**

```json
{
  "profile": {
    "id": 1,
    "fullname": "Nguyen Van A",
    "gender": "MALE",
    "phone": "0901234567"
  },
  "medical_history": {
    "items": [
      {
        "id": 1,
        "date": "2026-04-15",
        "doctor": "BS. Nguyễn Minh Khoa",
        "status": "COMPLETED",
        "payment": "PAID",
        "start_time": "08:00",
        "end_time": "09:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 25
    }
  }
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Invalid page" }` |
| `400` | `{ "error": "Invalid per_page" }` |

---

### 3.2. Update Patient Profile

Cập nhật hồ sơ bệnh nhân.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Request Body**

```json
{
  "fullname": "Nguyen Van A",
  "date_of_birth": "2002-05-10",
  "address": "Ho Chi Minh City",
  "phone_number": "0901234567"
}
```

**Response `200 OK`**

```json
{
  "fullname": "Nguyen Van A",
  "address": "Ho Chi Minh City",
  "date_of_birth": "2002-05-10",
  "patient_id": 1,
  "phone_number": "0901234567",
  "email": "patient@gmail.com"
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "You can not update gender" }` |
| `400` | `{ "error": "No data provided" }` |

---

## 4. Medical History

### 4.1. Get Medical History

Xem bệnh án sau khi hoàn thành khám.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Path Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `id` | `integer` | v | ID lịch khám |

**Response `200 OK`**

```json
{
  "appointment_id": 10,
  "diagnosis": "Viêm họng",
  "prescription": [
    {
      "medicine_name": "Paracetamol",
      "dosage": "2 lần/ngày"
    }
  ],
  "test_results": [
    {
      "test_name": "Blood Test",
      "result": "Normal"
    }
  ]
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Medical history not available. Appointment not completed" }` |
| `403` | `{ "error": "Forbidden" }` |
| `404` | `{ "error": "Appointment not found" }` |

---

### 4.2. Create Review

Đánh giá bác sĩ sau khi khám xong.

> 🔐 **Yêu cầu xác thực** – Role: `PATIENT`

**Path Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `id` | `integer` | v | ID lịch khám |

**Request Body**

```json
{
  "rating": 5,
  "comment": "Bác sĩ rất tận tình"
}
```

**Response `200 OK`**

```json
{
  "review_id": 3,
  "message": "Review success"
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Only completed appointment can review" }` |
| `400` | `{ "error": "Rating is required" }` |
| `403` | `{ "error": "Forbidden" }` |

---

### 4.3. Get Doctor Reviews

Lấy danh sách đánh giá của bác sĩ.

> 🔓 **Không yêu cầu xác thực**

**Path Parameters**

| Parameter | Type | Required | Description |
|:--|:--|:--:|:--|
| `id` | `integer` | v | ID bác sĩ |

**Response `200 OK`**

```json
{
  "doctor_id": 2,
  "average_rating": 4.5,
  "total_reviews": 20,
  "rating_breakdown": {
    "1": 0,
    "2": 1,
    "3": 3,
    "4": 7,
    "5": 9
  },
  "reviews": [
    {
      "id": 1,
      "rating": 5,
      "comment": "Bác sĩ rất tận tình",
      "created_date": "2026-04-27"
    }
  ]
}
```

**Response `404 Not Found`**

```json
{
  "error": "Doctor not found"
}
```

---

## Common Error Responses

| Status Code | Ý nghĩa | Response Body |
|:--:|:--|:--|
| `400` | Bad Request – Dữ liệu không hợp lệ | `{ "error": "Invalid request" }` |
| `401` | Unauthorized – Thiếu hoặc sai token | `{ "error": "Unauthorized" }` |
| `403` | Forbidden – Không đủ quyền truy cập | `{ "error": "Forbidden" }` |
| `404` | Not Found – Không tìm thấy tài nguyên | `{ "error": "Not found" }` |
| `500` | Internal Server Error | `{ "error": "Internal server error" }` |

---

> **Lưu ý:**
> - Các endpoint có 🔐 yêu cầu JWT token hợp lệ với role `PATIENT`.
> - Các endpoint có 🔓 là public, không cần đăng nhập.
> - Bệnh nhân chỉ được truy cập dữ liệu của chính mình; truy cập dữ liệu người khác sẽ nhận `403 Forbidden`.