import pytest
from app.models import Examination, Payment, Prescription, PrescriptionDetail, TestRequest, TestStatusEnum
from app.db.db import db

@pytest.fixture
def auth_header(doctor_token):
    return {"Authorization": f"Bearer {doctor_token}"}

# CREATE EXAMINATION
def test_create_examination_success(client, auth_header, waiting_appointment):
    appt = waiting_appointment
    res = client.post("/api/doctor/examinations", json={
            "appointment_id": appt.id, 
            "diagnosis": "Cảm cúm"
            }, headers=auth_header)
    
    assert res.status_code == 201

    assert res.get_json()["diagnosis"] == "Cảm cúm"
    assert res.get_json()["appointment_id"] == appt.id

    assert appt.status == "IN_PROGRESS"

def test_create_examination_no_token(client, waiting_appointment):
    res = client.post("/api/doctor/examinations", json={
        "appointment_id": waiting_appointment.id,
        "diagnosis": "x"
        })
    
    assert res.status_code == 401
    
def test_create_examination_wrong_role(client, patient_token, waiting_appointment):
    res = client.post("/api/doctor/examinations", json={
        "appointment_id": waiting_appointment.id,
        "diagnosis": "x"
        }, headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_create_examination_duplicate(client, auth_header, waiting_appointment):
    exam = Examination(
        appointment_id=waiting_appointment.id,
        diagnosis="TEST EXAM"
    )
    db.session.add(exam)
    db.session.commit()
    
    res = client.post("/api/doctor/examinations", json={
            "appointment_id": exam.appointment_id, 
            "diagnosis": "Cảm lại"
            }, headers=auth_header)
    
    assert res.status_code == 400

    assert "already exist" in res.get_json()["error"]

def test_create_examination_missing_appointment_id(client, auth_header):
    res = client.post("/api/doctor/examinations", json={"diagnosis": "Cảm cúm"}, headers=auth_header)
    
    assert res.status_code == 400

    assert "appointment_id is required" in res.get_json()["error"]

@pytest.mark.parametrize("status", ["IN_PROGRESS", "PENDING_PAYMENT", "PENDING_RESULT", "COMPLETED", "CANCELED"])
def test_create_examination_wrong_status(client, auth_header, waiting_appointment, status):
    appointment = waiting_appointment
    appointment.status = status
    
    res = client.post("/api/doctor/examinations", json={
            "appointment_id": appointment.id,
            "diagnosis": "x"}, headers=auth_header)
    
    assert res.status_code == 400

    assert "Appointment is not in examinating" in res.get_json()["error"]

def test_create_examination_wrong_doctor(client, users, waiting_appointment):
    other_doctor = users["doctor_usernames"][1]

    doctor_login = client.post("/api/auth/login", json={
        "username": other_doctor,
        "password": "123"
    })

    token = doctor_login.get_json()["access_token"]

    res = client.post("/api/doctor/examinations", json={
        "appointment_id": waiting_appointment.id,
        "diagnosis": "x"
        }, headers={"Authorization": f"Bearer {token}"})
    
    assert res.status_code == 400

    assert "Doctor mismatch: Not your appointment" in res.get_json()["error"]

def test_create_examination_with_symptoms(client, auth_header, waiting_appointment):
    appt = waiting_appointment

    res = client.post("/api/doctor/examinations", json={
        "appointment_id": appt.id,
        "diagnosis": "x",
        "symptoms": "Update Symptoms"
        }, headers=auth_header)
    
    assert res.status_code == 201

    assert res.get_json()["symptoms"] == "Update Symptoms"

def test_create_examination_request_body_required(client, auth_header):
    res = client.post("/api/doctor/examinations", json={}, headers=auth_header)

    assert res.status_code == 400
    assert "Request body is required" in res.get_json()["error"]

def test_create_examination_appointment_not_found(client, auth_header):
    res = client.post("/api/doctor/examinations", json={
        "appointment_id": 999999,
        "diagnosis": "abc"
    }, headers=auth_header)

    assert res.status_code == 400

    assert "Appointment not found" in res.get_json()["error"]

def test_create_examination_empty_diagnosis(client, auth_header, waiting_appointment):
    res = client.post("/api/doctor/examinations", json={
        "appointment_id": waiting_appointment.id
    }, headers=auth_header)

    assert res.status_code == 201

    assert res.get_json()["diagnosis"] == ""

def test_create_examination_symptoms_none(client, auth_header, waiting_appointment):
    res = client.post("/api/doctor/examinations", json={
        "appointment_id": waiting_appointment.id,
        "diagnosis": "Test",
        "symptoms": None
    }, headers=auth_header)

    assert res.status_code == 201
    
    assert res.get_json()["symptoms"] is None

# UPDATE EXAMINATION
def test_update_examination_success(client, auth_header, in_progress_examination):
    exam = in_progress_examination

    res = client.patch(f"/api/doctor/examinations/{exam.id}", json={
        "diagnosis": "Updated Examination",
        "symptoms": "Updated Symptoms"
    }, headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert "Updated Examination" in data["diagnosis"]
    assert "Updated Symptoms" in data["symptoms"]

@pytest.mark.parametrize("field", ["diagnosis", "symptoms"])
def test_update_examination_partial_data(client, auth_header, in_progress_examination, field):
    exam = in_progress_examination

    res = client.patch(f"/api/doctor/examinations/{exam.id}", json={
        f"{field}": "Updated"
    }, headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert "Updated" == data[f"{field}"]

def test_update_examination_empty_body(client, auth_header, in_progress_examination):
    exam = in_progress_examination

    old_diagnosis = exam.diagnosis

    res = client.patch(f"/api/doctor/examinations/{exam.id}", json={}, headers=auth_header)

    assert res.status_code == 200

    assert res.get_json()["diagnosis"] == old_diagnosis

def test_update_examination_status_pending_result(client, auth_header, in_progress_examination):
    exam = in_progress_examination
    exam.appointment.status = "PENDING_RESULT"
    db.session.commit()

    res = client.patch( f"/api/doctor/examinations/{exam.id}", json={
        "diagnosis": "Allowed Update"
        }, headers=auth_header)

    assert res.status_code == 200

    assert res.get_json()["diagnosis"] == "Allowed Update"

def test_update_examination_no_token(client, in_progress_examination):
    exam = in_progress_examination

    res = client.patch(f"/api/doctor/examinations/{exam.id}", json={
        "diagnosis": "Updated Examination",
        "symptoms": "Updated Symptoms"
    })

    assert res.status_code == 401

def test_update_examination_wrong_role(client, patient_token, in_progress_examination):
    exam = in_progress_examination

    res = client.patch(f"/api/doctor/examinations/{exam.id}", json={
        "diagnosis": "Updated Examination",
        "symptoms": "Updated Symptoms"
    }, headers={"Authorization": f"Bearer {patient_token}"})

    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_update_examination_wrong_doctor(client, users, in_progress_examination):
    user_login = client.post("/api/auth/login", json={
        "username": users["doctor_usernames"][1],
        "password": "123"
    })
    
    token = user_login.get_json()["access_token"]

    exam = in_progress_examination

    res = client.patch(f"/api/doctor/examinations/{exam.id}", json={
        "diagnosis": "Updated Examination",
        "symptoms": "Updated Symptoms"
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400

    assert "Doctor mismatch" in res.get_json()["error"]

@pytest.mark.parametrize("status", ["WAITING_EXAMINATION", "PENDING_PAYMENT", "COMPLETED", "CANCELED"])
def test_update_examination_wrong_status(client, auth_header, in_progress_examination, status):
    exam = in_progress_examination
    appt = exam.appointment

    appt.status = status
    db.session.commit()

    res = client.patch(f"/api/doctor/examinations/{exam.id}", json={
        "diagnosis": "Updated Examination",
        "symptoms": "Updated Symptoms"
    }, headers=auth_header)

    assert res.status_code == 400

    assert "Cannot update appointment" in res.get_json()["error"]

def test_update_examination_not_found(client, auth_header):
    res = client.patch("/api/doctor/examinations/999999", json={
        "diagnosis": "Updated"
        }, headers=auth_header)

    assert res.status_code == 400

    assert "Examination not found" in res.get_json()["error"]

# SAVE EXAMINATION
def test_save_examination_success(client, auth_header, in_progress_examination, prescription_detail, in_progress_test_request):
    exam = in_progress_examination

    res = client.post(f"/api/doctor/examinations/{exam.id}/save", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    # medicine:
    # Paracetamol 10000 * 2 = 20000
    # Vitamin C 15000 * 1 = 15000
    # total = 35000
    assert data["medicine"] == 35000

    # lab test:
    # Xét nghiệm máu = 50000
    assert data["lab_test"] == 50000

    medicine_payment = Payment.query.filter_by(
        appointment_id=exam.appointment_id,
        payment_type="MEDICINE"
    ).first()

    lab_payment = Payment.query.filter_by(
        appointment_id=exam.appointment_id,
        payment_type="LAB_TEST"
    ).first()

    assert medicine_payment is not None
    assert medicine_payment.amount == 35000
    assert medicine_payment.status == "PENDING"

    assert lab_payment is not None
    assert lab_payment.amount == 50000

def test_save_examination_not_found(client, auth_header):
    res = client.post("/api/doctor/examinations/99999/save",headers=auth_header)

    assert res.status_code == 400

    data = res.get_json()

    assert "Examination not found" in data["error"]

def test_save_examination_doctor_mismatch(client, users, in_progress_examination, prescription_detail):
    other_doctor = users["doctor_usernames"][1]

    doctor_login = client.post("/api/auth/login", json={
        "username": other_doctor,
        "password": "123"
    })

    token = doctor_login.get_json()["access_token"]
    
    exam = in_progress_examination

    res = client.post(f"/api/doctor/examinations/{exam.id}/save", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400

    data = res.get_json()

    assert "Doctor mismatch" in data["error"]

def test_save_examination_invalid_status(client, auth_header, completed_examination, prescription_with_completed_exam):
    exam = completed_examination

    res = client.post(f"/api/doctor/examinations/{exam.id}/save", headers=auth_header)

    assert res.status_code == 400

    data = res.get_json()

    assert "Cannot save" in data["error"]

def test_save_examination_without_prescription(client, auth_header, in_progress_examination):
    exam = in_progress_examination

    res = client.post(f"/api/doctor/examinations/{exam.id}/save", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert data["medicine"] == 0
    assert data["lab_test"] == 0

def test_save_examination_upsert_payment(client, auth_header, in_progress_examination, prescription_detail):
    exam = in_progress_examination

    old_payment = Payment(
        appointment_id=exam.appointment_id,
        payment_type="MEDICINE",
        amount=1000,
        status="PENDING"
    )

    db.session.add(old_payment)
    db.session.commit()

    response = client.post(f"/api/doctor/examinations/{exam.id}/save", headers=auth_header)

    assert response.status_code == 200

    payments = Payment.query.filter_by(
        appointment_id=exam.appointment_id,
        payment_type="MEDICINE",
        status="PENDING"
    ).all()

    # phải chỉ có 1 payment
    assert len(payments) == 1

    # amount được update
    assert payments[0].amount == 35000

def test_save_examination_forbidden_role(client, patient_token, in_progress_examination):
    exam = in_progress_examination

    response = client.post(f"/api/doctor/examinations/{exam.id}/save", headers={"Authorization": f"Bearer {patient_token}"})

    assert response.status_code == 403

    data = response.get_json()

    assert data["error"] == "Forbidden"







