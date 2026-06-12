# Clinic Management System

## Overview

Clinic Management System is a RESTful web application designed to streamline clinic operations by digitizing appointment booking, medical examinations, prescriptions, laboratory requests, and clinic administration.

The system helps reduce waiting times, improve patient experience, and provide doctors with efficient tools to manage consultations, prescriptions, and diagnostic workflows.

This project was developed as a Software Testing and Backend Development capstone project, with a strong focus on API design, business workflows, and software quality assurance.

---

## Key Features

### Patient Module

* Register and authenticate accounts
* Browse doctors and specialties
* Book appointments online
* Pay appointment deposits
* View appointment history
* View prescriptions and examination results
* Submit doctor reviews and ratings

### Doctor Module

* View daily appointment schedules
* Manage monthly working calendars
* Create and update examinations
* Record diagnoses and symptoms
* Create electronic prescriptions
* Request laboratory tests
* Review laboratory results
* Complete medical consultations

### Admin Module

* Manage doctors
* Manage specialties
* Manage medicines
* Manage laboratory tests
* Monitor appointments and clinic operations

---

## System Architecture

The application follows a layered Client–Server architecture using RESTful APIs.

```text
Client (Web / Mobile)
        │
        ▼
REST API (Flask)
        │
 ┌──────┴──────┐
 │   Routes    │
 │ Controllers │
 └──────┬──────┘
        │
        ▼
   DAO Layer
(Business Logic)
        │
        ▼
 SQLAlchemy ORM
        │
        ▼
      MySQL
```

### Architectural Patterns

* Client–Server Architecture
* RESTful API Design
* DAO (Data Access Object) Pattern
* JWT Authentication
* Layered Architecture

---

## Technology Stack

### Backend

* Python
* Flask
* Flask-JWT-Extended
* SQLAlchemy
* MySQL

### Testing

* Pytest
* Unit Testing
* Integration Testing
* Manual Testing
* API Testing (Postman)

### Development Tools

* Git & GitHub
* Postman
* Swagger / API Documentation
* MySQL Workbench

---

## Authentication

The system uses JWT-based authentication.

Example:

```http
Authorization: Bearer <access_token>
```

Role-based authorization is implemented for:

* Patient
* Doctor
* Admin

---

## Main Business Workflow

```text
Patient
   │
   ▼
Book Appointment
   │
   ▼
Pay Deposit
   │
   ▼
Doctor Consultation
   │
   ├── Diagnosis
   ├── Prescription
   └── Lab Test Request
   │
   ▼
Receive Results
   │
   ▼
Complete Appointment
```

---

## Database Entities

Core entities include:

* User
* Patient
* Doctor
* Specialization
* Appointment
* TimeSlot
* DoctorSchedule
* Examination
* Prescription
* PrescriptionDetail
* Medicine
* Test
* TestRequest
* Review
* Payment

---

## Testing

The project includes multiple testing levels:

### Manual Testing

* Functional Testing
* Negative Testing
* Authorization Testing
* Boundary Value Analysis
* Equivalence Partitioning

### Automated Testing

Implemented using Pytest:

#### Unit Testing

Testing individual business logic and DAO functions.

#### Integration Testing

Testing API endpoints and database interactions.

Examples:

* Appointment Management
* Examination Management
* Prescription Management
* Laboratory Test Requests
* Authentication & Authorization

---

## API Modules

### Authentication API

```http
POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
```

### Patient API

```http
GET    /api/patient/doctors
POST   /api/patient/appointments
GET    /api/patient/history
POST   /api/patient/reviews
```

### Doctor API

```http
GET    /api/doctor/profile
PATCH  /api/doctor/profile

GET    /api/doctor/appointments
GET    /api/doctor/appointments/{id}

POST   /api/doctor/examinations
PATCH  /api/doctor/examinations/{id}

POST   /api/doctor/examinations/{id}/prescriptions
POST   /api/doctor/examinations/{id}/lab-tests

POST   /api/doctor/appointments/{id}/complete
```

### Admin API

```http
CRUD /api/admin/doctors
CRUD /api/admin/specializations
CRUD /api/admin/medicines
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/clinic-management-system.git
cd clinic-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

```bash
source venv/bin/activate
```

or

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=clinic_db
MYSQL_USER=root
MYSQL_PASSWORD=password

JWT_SECRET_KEY=your_jwt_secret
```

### Run Database Migration

```bash
flask db upgrade
```

### Start Server

```bash
python run.py
```

Application will run at:

```text
http://localhost:5000
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Generate coverage report:

```bash
pytest --cov=app
```

Generate HTML coverage:

```bash
pytest --cov=app --cov-report=html
```

---

## Learning Outcomes

Through this project, the team gained practical experience in:

* RESTful API Development
* Backend System Design
* Database Modeling
* JWT Authentication & Authorization
* Software Testing Practices
* Unit & Integration Testing
* Healthcare Workflow Modeling
* Git Collaboration & Team Development

---

## Authors
Ngo Hoang Kieu Trang
Nguyen Thanh Nhi
Team Size: 2 Members

Role:

* Backend Development
* API Design
* Database Design
* Testing & Quality Assurance
