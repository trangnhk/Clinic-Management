# Auth API Documentation

> **Clinic Management System** – Authentication API Reference

---

## Overview

| Thông tin | Chi tiết |
|:--|:--|
| **Base URL** | `/api/auth` |
| **Authentication** | Không yêu cầu |

---

## Table of Contents

- [POST /register](#1-register-user)
- [POST /login](#2-login-user)
- [JWT Authentication Usage](#jwt-authentication-usage)
- [User Roles](#user-roles)
- [Authentication Flow](#authentication-flow)

---

## 1. Register User

Đăng ký tài khoản người dùng mới trong hệ thống.

>  **Không yêu cầu xác thực**

**Request Body**

```json
{
  "username": "user01",
  "email": "user01@gmail.com",
  "password": "123456"
}
```

**Request Body Fields**

| Field | Type | Required | Description |
|:--|:--|:--:|:--|
| `username` | `string` | v | Tên đăng nhập |
| `email` | `string` | v | Email người dùng |
| `password` | `string` | v | Mật khẩu tài khoản |

**Response `200 OK`**

```json
{
  "id": 1,
  "username": "user01",
  "email": "user01@gmail.com",
  "role": "PATIENT"
}
```

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Username already exists" }` |
| `400` | `{ "error": "Email already exists" }` |
| `400` | `{ "error": "Password is required" }` |

---

## 2. Login User

Đăng nhập vào hệ thống và nhận JWT Access Token.

>  **Không yêu cầu xác thực**

**Request Body**

```json
{
  "username": "user01",
  "password": "123456"
}
```

**Request Body Fields**

| Field | Type | Required | Description |
|:--|:--|:--:|:--|
| `username` | `string` | v | Tên đăng nhập |
| `password` | `string` | v | Mật khẩu |

**Response `200 OK`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "user01",
    "role": "PATIENT"
  }
}
```

**Response Fields**

| Field | Type | Description |
|:--|:--|:--|
| `access_token` | `string` | JWT Access Token |
| `user.id` | `integer` | ID người dùng |
| `user.username` | `string` | Username |
| `user.role` | `string` | Vai trò người dùng |

**Error Responses**

| Status | Response |
|:--|:--|
| `400` | `{ "error": "Missing username" }` |
| `400` | `{ "error": "Missing password" }` |
| `401` | `{ "error": "Invalid" }` |

---

## JWT Authentication Usage

Sau khi đăng nhập thành công, đính kèm JWT token vào header của mọi request tới các Protected API:

```http
Authorization: Bearer <access_token>
```

---

## User Roles

| Role | Description |
|:--|:--|
| `PATIENT` | Bệnh nhân |
| `DOCTOR` | Bác sĩ |
| `ADMIN` | Quản trị viên |

---

## Authentication Flow
Register -> Login -> Receive JWT Token -> Access Protected APIs

> **Lưu ý:** JWT Token phải được gửi kèm trong mọi request tới các endpoint yêu cầu xác thực.
> Token không hợp lệ hoặc hết hạn sẽ nhận phản hồi `401 Unauthorized`.