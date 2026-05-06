import pytest
from app.db.db import db
from app.models import Payment
from datetime import datetime

@pytest.fixture
def auth_header(patient_token):
    return {"Authorization": f"Bearer {patient_token}"}

def test_get_medical_history_success(client, auth_header, completed_appointment ,payment_completed, completed_examination , prescription_with_completed_exam):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert "appointment_info" in data
    assert "patient_info" in data
    assert "doctor_info" in data
    assert "medical_result" in data
    assert "prescription" in data
    assert "payment" in data

def test_get_medical_history_diagnosis(client, auth_header, completed_appointment,completed_examination):
    res = client.get(f"/api/patient/appointments/{completed_appointment.id}/medical-history",
        headers=auth_header
    )

    data = res.get_json()

    assert data["medical_result"]["diagnosis"] == "Test Examination"

def test_get_medical_history_prescription_items_count(client, auth_header, completed_appointment ,payment_completed, completed_examination , prescription_with_completed_exam):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert len(data["prescription"]["items"]) == 2

def test_get_medical_history_total_medicine_cost(client, auth_header, completed_appointment ,payment_completed, completed_examination , prescription_with_completed_exam):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert data["prescription"]["total_medicine_cost"] == 35000.0

def test_get_medical_history_payment_info(client, auth_header, completed_appointment ,payment_completed, completed_examination , prescription_with_completed_exam):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 200

    payment = res.get_json()["payment"]
    prescription = res.get_json()["prescription"]

    assert len(payment["items"]) == 3

    assert payment["summary"]["deposit"] == 10000
    assert payment["summary"]["medicine"] == 35000
    assert payment["summary"]["final"] == 50000
    assert payment["total_paid"] == 60000

def test_get_medical_history_no_token(client, completed_appointment):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history")

    assert res.status_code == 401

def test_get_medical_history_wrong_role(client, doctor_token, completed_appointment):
    appt = completed_appointment
    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403

def test_get_medical_history_not_found(client, auth_header):
    res = client.get("/api/patient/appointments/9999/medical-history", headers=auth_header)

    assert res.status_code == 404

    assert "Appointment not found" in res.get_json()["error"]

def test_get_medical_history_not_owner(client, users, completed_appointment):
    user = client.post("/api/auth/login", json={
        "username": users["patient_usernames"][1],
        "password": "123"
    })

    token = user.get_json()["access_token"]
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_get_medical_history_appointment_not_completed(client, auth_header, paid_appointment):
    appt = paid_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 400

    assert "Medical history not available. Appointment not completed" in res.get_json()["error"]

def test_get_medical_history_no_examination(client, auth_header, completed_appointment):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 400

    assert "Examination not found" in res.get_json()["error"]

def test_get_medical_history_no_prescription(client, auth_header, completed_appointment, completed_examination):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 200

    prescription = res.get_json()["prescription"]

    assert prescription["items"] == []
    assert prescription["total_medicine_cost"] == 0

def test_get_medical_history_no_payment(client, auth_header, completed_appointment, completed_examination, prescription_with_completed_exam):
    appt = completed_appointment

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 200

    payment = res.get_json()["payment"]

    assert payment["items"] == []
    assert payment["total_paid"] == 0

def test_get_medical_history_ignore_failed_payment(client, auth_header, completed_appointment, completed_examination, prescription_with_completed_exam):
    appt = completed_appointment

    # Payment hợp lệ
    paid_payment = Payment(
        appointment_id=appt.id,
        payment_type="DEPOSIT",
        amount=100000,
        status="PAID"
    )

    # Payment lỗi -> phải ignore
    failed_payment = Payment(
        appointment_id=appt.id,
        payment_type="MEDICINE",
        amount=50000,
        status="FAILED"
    )

    db.session.add_all([paid_payment, failed_payment])
    db.session.commit()

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()
    payment = data["payment"]

    # chỉ lấy payment PAID
    assert payment["total_paid"] == 100000

    # chỉ có 1 item được trả ra
    assert len(payment["items"]) == 1

    # failed payment không xuất hiện
    assert payment["items"][0]["type"] == "DEPOSIT"

    # summary chỉ cộng payment PAID
    assert payment["summary"]["deposit"] == 100000
    assert payment["summary"]["medicine"] == 0

def test_get_medical_history_ignore_pending_payment(client, auth_header, completed_appointment, completed_examination, prescription_with_completed_exam):
    appt = completed_appointment

    paid_payment = Payment(
        appointment_id=completed_appointment.id,
        payment_type="DEPOSIT",
        amount=100000,
        status="PAID",
        paid_at=datetime.now()
    )
    pending_payment = Payment(
        appointment_id=completed_appointment.id,
        payment_type="LAB_TEST",
        amount=200000,
        status="PENDING"
    )
    db.session.add_all([paid_payment, pending_payment])
    db.session.commit()

    res = client.get(f"/api/patient/appointments/{appt.id}/medical-history",headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()
    payment = data["payment"]

    # Chỉ cộng payment PAID
    assert payment["total_paid"] == 100000

    # Chỉ có 1 item hợp lệ
    assert len(payment["items"]) == 1

    assert payment["items"][0]["type"] == "DEPOSIT"
    assert payment["items"][0]["amount"] == 100000

    # Pending payment phải bị ignore
    assert payment["summary"]["deposit"] == 100000
    assert payment["summary"]["lab_test"] == 0
    assert payment["summary"]["medicine"] == 0
    assert payment["summary"]["final"] == 0

def test_get_medical_history_total_paid_equals_summary(client, auth_header, completed_appointment, completed_examination, payment_completed):
    res = client.get(f"/api/patient/appointments/{completed_appointment.id}/medical-history",headers=auth_header)
    
    assert res.status_code == 200

    payment = res.get_json()["payment"]

    total = (payment["summary"]["deposit"] + payment["summary"]["final"])

    assert total == payment["total_paid"]

