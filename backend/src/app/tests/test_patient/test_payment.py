import pytest
from datetime import timedelta, datetime
from app.models import Appointment, Payment, DoctorSchedule, SlotStatusEnum, AppointmentStatusEnum, PaymentStatusEnum, PaymentTypeEnum
from app.db.db import db
from app.modules.patient.dao import auto_cancel_unpaid

@pytest.fixture
def auth_header(patient_token):
    return {"Authorization": f"Bearer {patient_token}"}

def test_make_payment_success(client, auth_header, pending_payment_appointment):
    appt = pending_payment_appointment

    res = client.post("/api/patient/payments", json={
        "appointment_id": appt.id,
        "amount": 150000
    }, headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert data["status"] == "PAID"
    assert data["payment_type"] == "DEPOSIT"

    updated = Appointment.query.get(appt.id)

    assert updated.status == AppointmentStatusEnum.WAITING_EXAMINATION
    assert updated.payment_status == PaymentStatusEnum.PAID

def test_make_payment_create_record(client, auth_header, pending_payment_appointment):
    appt = pending_payment_appointment

    client.post("/api/patient/payments", json={
        "appointment_id": appt.id,
        "amount": 200000
    }, headers=auth_header)

    payment = Payment.query.filter_by(appointment_id=appt.id).first()

    assert payment is not None
    assert payment.amount == 200000
    assert payment.payment_type == PaymentTypeEnum.DEPOSIT

def test_make_payment_no_token(client, pending_payment_appointment):
    res = client.post("/api/patient/payments", json={
            "appointment_id": pending_payment_appointment.id,
            "amount": 150000
        })

    assert res.status_code == 401

def test_make_payment_wrong_role(client, doctor_token, pending_payment_appointment):
    res = client.post("/api/patient/payments", json={
            "appointment_id": pending_payment_appointment.id,
            "amount": 150000
        },
        headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403
    assert "Forbidden" in res.get_json()["error"]

def test_make_payment_missing_appointment_id(client, auth_header):
    res = client.post("/api/patient/payments", json={
            "amount": 150000
        }, headers=auth_header)

    assert res.status_code == 400
    assert "Missing required fields" in res.get_json()["error"]

def test_make_payment_missing_amount(client, auth_header):
    res = client.post("/api/patient/payments", json={
            "appointment_id": 1
        }, headers=auth_header)

    assert res.status_code == 400
    assert "Missing required fields" in res.get_json()["error"]


def test_make_payment_missing_both_fields(client, auth_header):
    res = client.post("/api/patient/payments", json={}, headers=auth_header)

    assert res.status_code == 400


def test_make_payment_minimum_fail(client, auth_header, pending_payment_appointment):
    res = client.post("/api/patient/payments", json={
        "appointment_id": pending_payment_appointment.id,
        "amount": 99999
    }, headers=auth_header)

    assert res.status_code == 400


def test_make_payment_exact_minimum_success(client, auth_header, pending_payment_appointment):
    res = client.post("/api/patient/payments", json={
            "appointment_id": pending_payment_appointment.id,
            "amount": 100000
        }, headers=auth_header)

    assert res.status_code == 200


def test_make_payment_appointment_not_found(client, auth_header):
    res = client.post("/api/patient/payments", json={
            "appointment_id": 999999,
            "amount": 150000
        }, headers=auth_header)

    assert res.status_code == 400
    assert "Appointment not found" in res.get_json()["error"]


def test_make_payment_not_owner(client, users, appointments):
    # patient1 login
    login = client.post("/api/auth/login", json={
            "username": users["patient_usernames"][1],
            "password": "123"
        })

    token = login.get_json()["access_token"]

    appt = appointments[0]
    appt.patient_id = users["patients"][0].id
    appt.status = "PENDING_PAYMENT"
    db.session.commit()

    res = client.post("/api/patient/payments", json={
            "appointment_id": appt.id,
            "amount": 150000
        }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400
    assert "Not your appointment" in res.get_json()["error"]


def test_make_payment_already_paid(client, auth_header, paid_appointment):
    res = client.post("/api/patient/payments", json={
        "appointment_id": paid_appointment.id,
        "amount": 150000
    }, headers=auth_header)

    assert res.status_code == 400


@pytest.mark.parametrize("status", ["WAITING_EXAMINATION", "COMPLETED", "CANCELED"])
def test_make_payment_invalid_status(client, auth_header, appointments, status):
    appt = appointments[0]
    appt.status = status
    appt.payment_status = "PENDING"
    db.session.commit()

    res = client.post("/api/patient/payments", json={
            "appointment_id": appt.id,
            "amount": 150000
        }, headers=auth_header)

    assert res.status_code == 400
    assert "Invalid appointment status" in res.get_json()["error"]


def test_make_payment_twice(client, auth_header, pending_payment_appointment):
    appt = pending_payment_appointment

    first = client.post("/api/patient/payments", json={
            "appointment_id": appt.id,
            "amount": 150000
        }, headers=auth_header)

    assert first.status_code == 200

    second = client.post("/api/patient/payments", json={
            "appointment_id": appt.id,
            "amount": 150000
        }, headers=auth_header)

    assert second.status_code == 400


def test_auto_cancel_unpaid_success(app, pending_payment_appointment):
    appt = pending_payment_appointment
    appt.created_at = datetime.now() - timedelta(minutes=31)

    db.session.commit()

    auto_cancel_unpaid()

    updated = Appointment.query.get(appt.id)

    assert updated.status == AppointmentStatusEnum.CANCELED
    assert updated.payment_status == PaymentStatusEnum.FAILED


def test_auto_cancel_unpaid_release_schedule(app, pending_payment_appointment):
    appt = pending_payment_appointment
    appt.created_at = datetime.now() - timedelta(minutes=31)

    schedule = DoctorSchedule.query.filter_by(
        doctor_id=appt.doctor_id,
        date=appt.date,
        timeslot_id=appt.timeslot_id).first()

    if schedule:
        schedule.status = SlotStatusEnum.BOOKED

    db.session.commit()

    auto_cancel_unpaid()

    schedule = DoctorSchedule.query.filter_by(
        doctor_id=appt.doctor_id,
        date=appt.date,
        timeslot_id=appt.timeslot_id
        ).first()

    assert schedule.status == SlotStatusEnum.AVAILABLE


def test_auto_cancel_unpaid_not_expired(app, pending_payment_appointment):
    appt = pending_payment_appointment
    appt.created_at = datetime.now() - timedelta(minutes=10)

    db.session.commit()

    auto_cancel_unpaid()

    updated = Appointment.query.get(appt.id)

    assert updated.status == "PENDING_PAYMENT"


def test_auto_cancel_unpaid_ignore_paid(app, pending_payment_appointment):
    appt = pending_payment_appointment
    appt.created_at = datetime.now() - timedelta(minutes=31)
    appt.payment_status = "PAID"
    appt.status = "WAITING_EXAMINATION"

    db.session.commit()

    auto_cancel_unpaid()

    updated = Appointment.query.get(appt.id)

    assert updated.status == "WAITING_EXAMINATION"