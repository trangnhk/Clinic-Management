import pytest
from app.db.db import db
from datetime import date
from app.models import Prescription, PrescriptionDetail

today = date.today()

@pytest.fixture
def auth_header(doctor_token):
    return {"Authorization": f"Bearer {doctor_token}"}


# GET APPOINTMENT
def test_get_appointments_success(client, auth_header, appointments):
    res = client.get(f"/api/doctor/appointments?date={today}", headers=auth_header)
    
    assert res.status_code == 200

    assert isinstance(res.get_json(), list)

@pytest.mark.parametrize("status", ["WAITING_EXAMINATION", "COMPLETED", "IN_PROGRESS", "PENDING_RESULT"])
def test_get_appointments_with_status_filter(client, auth_header, appointments, users, status):
    doctor0 = users["doctors"][0]

    expected_count = sum(
        1 for a in appointments
        if a.doctor_id == doctor0.id
        and (a.status.value if hasattr(a.status, "value") else a.status) == status
        and a.date == today
    )

    res = client.get(f"/api/doctor/appointments?date={today}&status={status}", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)

    for a in data:
        assert a["status"] == status

    assert len(data) == expected_count

def test_get_appointments_forbidden(client, patient_token):
    res = client.get(f"/api/doctor/appointments?date={today}", headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_get_appointments_no_token(client):
    res = client.get(f"/api/doctor/appointments?date={today}")
    
    assert res.status_code == 401

def test_get_appointments_missing_date(client, auth_header):
    res = client.get("/api/doctor/appointments", headers=auth_header)

    assert res.status_code == 400

    assert "Missing date" in res.get_json()["error"]

def test_get_appointments_invalid_date_format(client, auth_header):
    res = client.get("/api/doctor/appointments?date=01-05-2026", headers=auth_header)

    assert res.status_code == 400

    assert "Invalid date format" in res.get_json()["error"]

@pytest.mark.parametrize("status", ["CANCELED", "PENDING_PAYMENT"])
def test_get_appointments_with_wrong_status(client, auth_header, appointments, users, status):
    doctor0 = users["doctors"][0]

    res = client.get(f"/api/doctor/appointments?date={today}&status={status}", headers=auth_header)

    assert res.status_code == 403
    
    assert "Forbidden" in res.get_json()["error"]

def test_get_appointments_response_has_can_examine(client, auth_header, doctor_appointments):
    res = client.get(f"/api/doctor/appointments?date={today}", headers=auth_header)
    
    data = res.get_json()

    assert len(data) >= 1
    
    item = data[0]
    assert "can_examine" in item
    assert "can_complete" in item
    assert "patient" in item

def test_get_appointments_doctor_not_found(client, auth_header, users):
    doctor = users["doctors"][0]
    db.session.delete(doctor)
    db.session.commit()

    res = client.get(f"/api/doctor/appointments?date={today}", headers=auth_header)

    assert res.status_code == 404

    assert "Doctor not found" in res.get_json()["error"]

# GET APPOINTMENT DETAIL
def test_get_appointment_detail_success(client, auth_header, waiting_appointment):
    res = client.get(f"/api/doctor/appointments/{waiting_appointment.id}", headers=auth_header)
    
    assert res.status_code == 200

    assert "patient" in res.json

    assert "examination" in res.json

def test_get_appointment_detail_success_no_examination(client, auth_header, waiting_appointment):
    res = client.get(f"/api/doctor/appointments/{waiting_appointment.id}", headers=auth_header)

    assert res.status_code == 200

    assert res.json["appointment_id"] == waiting_appointment.id
    assert res.json["examination"] is None

def test_get_appointment_detail_exam_without_prescription_success(client, auth_header, in_progress_examination):
    appt_id = in_progress_examination.appointment_id
    res = client.get(f"/api/doctor/appointments/{appt_id}", headers=auth_header)

    assert res.status_code == 200
    assert res.json["examination"]["diagnosis"] == "Test in progress examination"

    assert res.json["examination"]["prescription"] is None

def test_get_appointment_detail_full_data(client, auth_header, in_progress_examination, prescription_detail, in_progress_test_request):
    appt = in_progress_examination.appointment
    res = client.get(f"/api/doctor/appointments/{appt.id}", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert data["examination"] is not None
    assert data["examination"]["diagnosis"] == "Test in progress examination"

    # Prescription
    pres = data["examination"]["prescription"]
    assert pres is not None
    assert len(pres["details"]) == 2

    # Tổng tiền thuốc
    assert pres["total_medicine_cost"] == 35000

    # phí khám
    assert pres["consultation_fee"] == 500000

    # tổng bill
    assert pres["total"] == 535000

    # lab test
    assert len(data["examination"]["lab_tests"]) == 1
    assert data["examination"]["lab_tests"][0]["status"] == "IN_PROGRESS"

def test_get_appointment_detail_not_found(client, auth_header):
    res = client.get("/api/doctor/appointments/99999", headers=auth_header)
    
    assert res.status_code == 400

    assert "Appointment not found" in res.get_json()["error"]

def test_get_appointment_detail_wrong_doctor(client, users, waiting_appointment):
    other_doctor = users["doctor_usernames"][1]

    doctor_login = client.post("/api/auth/login", json={
        "username": other_doctor,
        "password": "123"
    })

    token = doctor_login.get_json()["access_token"]

    res = client.get(f"/api/doctor/appointments/{waiting_appointment.id}", headers={"Authorization": f"Bearer {token}"})
    
    assert res.status_code == 400
    
    assert "Forbidden" in res.json["error"]

def test_get_appointment_detail_wrong_role(client, users, waiting_appointment, patient_token):
    res = client.get(f"/api/doctor/appointments/{waiting_appointment.id}", headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403
    
    assert "Forbidden" in res.json["error"]

def test_get_appointment_detail_no_token(client, users, waiting_appointment):
    res = client.get(f"/api/doctor/appointments/{waiting_appointment.id}")
    
    assert res.status_code == 401


# COMPLETE APPOINTMENT
def test_complete_appointment_success(client, auth_header, in_progress_examination):
    appt_id = in_progress_examination.appointment_id

    res = client.post(f"/api/doctor/appointments/{appt_id}/complete",
        headers=auth_header)
    
    assert res.status_code == 200

    assert res.get_json()["status"] == "COMPLETED"
    assert res.get_json()["message"] == "Appointment completed successfully"

def test_complete_appointment_wrong_role(client, patient_token, in_progress_examination):
    appt_id = in_progress_examination.appointment_id

    res = client.post(f"/api/doctor/appointments/{appt_id}/complete",
        headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403

def test_complete_appointment_no_token(client, in_progress_examination):
    appt_id = in_progress_examination.appointment_id

    res = client.post(f"/api/doctor/appointments/{appt_id}/complete")
    
    assert res.status_code == 401

def test_complete_appointment_no_examination(client, auth_header, in_progress_appointment):
    res = client.post(f"/api/doctor/appointments/{in_progress_appointment.id}/complete",
        headers=auth_header)
    assert res.status_code == 400
    assert "examination not created" in res.get_json()["error"]

def test_complete_appointment_already_completed(client, auth_header, in_progress_examination):
    appt = in_progress_examination.appointment
    appt.status = "COMPLETED"

    db.session.commit()

    res = client.post(f"/api/doctor/appointments/{appt.id}/complete",
        headers=auth_header)
    assert res.status_code == 400
    assert "already completed" in res.get_json()["error"]

def test_complete_appointment_pending_lab_tests(client, auth_header, in_progress_test_request):
    appt_id = in_progress_test_request.appointment_id
    res = client.post(f"/api/doctor/appointments/{appt_id}/complete",
        headers=auth_header)
    assert res.status_code == 400
    assert "lab test" in res.get_json()["error"]










