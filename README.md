# Clinic Management System

## Overview

Clinic Management System is a RESTful web application developed to support the daily operations of a medical clinic.

The system allows patients to book appointments online, doctors to manage consultations and prescriptions, and administrators to manage clinic resources such as doctors, specialties, and medicines.

The project was developed as a Software Testing and Backend Development capstone project with a strong focus on API design, business workflows, and software quality assurance.

---

## Features

### Patient Features

* Register account
* Login using JWT authentication
* View doctor list
* Book appointments online
* View appointment history
* View prescriptions

### Doctor Features

* View assigned appointments
* Create examinations
* Record diagnosis information
* Create prescriptions for patients

### Admin Features

* Manage doctors
* Manage specialties
* Manage medicines
* Manage schedules and time slots through Flask-Admin

---

## System Architecture

The application follows a layered Client–Server architecture.

```text
Client
(Web / Mobile / Postman)

        │
        ▼

REST API (Flask)

        │
        ▼

Routes Layer

        │
        ▼

DAO Layer
(Business Logic)

        │
        ▼

SQLAlchemy ORM

        │
        ▼

MySQL Database
```

### Design Patterns

* Client–Server Architecture
* RESTful API Design
* DAO Pattern
* Layered Architecture
* JWT Authentication

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
* API Testing
* Manual Testing

### Tools

* Git
* GitHub
* Postman
* Swagger (Flasgger)
* MySQL Workbench

---

## Authentication

JWT Authentication is used for securing APIs.

Example:

```http
Authorization: Bearer <access_token>
```

Role-based authorization:

* PATIENT
* DOCTOR
* ADMIN

---

## Main Workflow

```text
Patient
   │
   ▼
Book Appointment
   │
   ▼
Doctor Views Appointment
   │
   ▼
Create Examination
   │
   ▼
Create Prescription
   │
   ▼
Patient Views Prescription
```

---

## Database Entities

### User Management

* User
* Patient
* Doctor

### Appointment Management

* Appointment
* DoctorSchedule
* TimeSlot

### Medical Records

* Examination
* Prescription
* PrescriptionDetail

### Administration

* Specialization
* Medicine

---

## API Endpoints

### Authentication

```http
POST /api/auth/register
POST /api/auth/login
```

---

### Patient APIs

```http
GET  /api/patient/doctors
POST /api/patient/appointments
GET  /api/patient/history
GET  /api/patient/prescriptions
```

---

### Doctor APIs

```http
GET  /api/doctor/appointments

POST /api/doctor/examinations

POST /api/doctor/prescriptions
```

---

### Admin Management

Managed through Flask-Admin:

```text
/admin
```

Available resources:

* Users
* Doctors
* Patients
* Specializations
* Medicines
* Doctor Schedules
* Time Slots

---

## Installation

### Clone Repository

```bash
git clone https://github.com/trangnhk/Clinic-Management.git

cd backend\src 
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=clinic_db
MYSQL_USER=root
MYSQL_PASSWORD=password
```

---

### Run Migration

```bash
flask db upgrade
```

---

### Start Application

```bash
python -m app.modules.main.main_tests
```

or

```bash
python run.py
```

---

Application URL:

```text
http://localhost:5000
```

Swagger:

```text
http://localhost:5000/apidocs
```

Admin:

```text
http://localhost:5000/admin
```

---

## Testing

### Manual Testing

Techniques used:

* Functional Testing
* Boundary Value Analysis
* Equivalence Partitioning
* Negative Testing
* Authorization Testing

### Automated Testing

Implemented using Pytest.

#### Unit Testing

Testing DAO and business logic functions.

Examples:

* Authentication
* Appointment creation
* Prescription creation

#### Integration Testing

Testing REST API endpoints and database interactions.

Examples:

* Authentication APIs
* Patient APIs
* Doctor APIs

---

## Learning Outcomes

Through this project, the team gained experience in:

* RESTful API Development
* Flask Backend Development
* Database Design
* JWT Authentication
* Role-Based Authorization
* Software Testing
* Unit Testing
* Integration Testing
* API Documentation
* Healthcare Workflow Modeling

---

## Authors

### Ngo Hoang Kieu Trang

* Backend Development
* API Design
* Database Design
* Testing

### Nguyen Thanh Nhi

* Backend Development
* API Testing
* Documentation
* Testing

Team Size: 2 Members
