import pytest
from datetime import timedelta, datetime, date
from app.models import *
from app.db.db import db

today = date.today()

@pytest.fixture
def auth_header(patient_token):
    return {"Authorization": f"Bearer {patient_token}"}

# BOOKING FLOW
def test_get_specializations(client, specializations):
    res = client.get("/api/patient/specializations")

    assert res.status_code == 200
    data = res.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert "name" in data[0]

def test_get_all_doctors(client, doctor_with_specs):
    res = client.get("/api/patient/doctors")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == len(doctor_with_specs)
    print(doctor_with_specs)

    for d in data:
        assert "id" in d
        assert "name" in d
        assert "specialization" in d

def test_get_doctors_by_specialization(client, specializations, doctor_with_specs):
    spec = specializations[0]
    
    res = client.get(f"/api/patient/doctors?specialization_id={spec.id}")
    
    assert res.status_code == 200
    data = res.get_json()

    assert isinstance(data, list)
    assert len(data) > 0

    for d in data:
        assert d["specialization"] == spec.name

def test_get_doctors_by_specialization_count(client, doctor_with_specs, specializations):
    spec = specializations[0]

    expected = [d for d in doctor_with_specs if d.specialization_id == spec.id]

    res = client.get(f"/api/patient/doctors?specialization_id={spec.id}")
    data = res.get_json()

    assert len(data) == len(expected)

def test_get_doctors_not_mixed_specialization(client, doctor_with_specs, specializations):
    spec = specializations[0]

    res = client.get(f"/api/patient/doctors?specialization_id={spec.id}")
    data = res.get_json()

    for d in data:
        assert d["specialization"] != specializations[1].name

def test_get_doctors_invalid_specialization(client):
    res = client.get("/api/patient/doctors?specialization_id=abc")

    assert res.status_code == 400

def test_get_doctors_specialization_not_found(client):
    res = client.get("/api/patient/doctors?specialization_id=999")

    assert res.status_code == 200
    assert res.get_json() == []

def test_get_timslots_success(client, users, timeslots, schedules):
    doctor = users["doctors"]
    doctor = doctor[0]

    # get doctor's schedule
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)
    date_str = schedule.date.strftime("%Y-%m-%d")

    res = client.get(f"/api/patient/timeslots?doctor_id={doctor.id}&date={date_str}")

    assert res.status_code == 200
    
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

    # check structure
    item = data[0]
    assert "schedule_id" in item
    assert "start_time" in item
    assert "end_time" in item
    assert "status" in item

    assert item["schedule_id"] == schedule.id

def test_get_timslots_doctor_not_found(client):
    res = client.get(f"/api/patient/timeslots?doctor_id=999&date={today}")

    assert res.status_code == 400
    
    assert "Doctor not found" in res.get_json()["error"]

def test_get_timeslots_missing_date(client):
    res = client.get("/api/patient/timeslots?doctor_id=1")

    assert res.status_code == 400

def test_get_timeslots_missing_doctor(client):
    res = client.get(f"/api/patient/timeslots?date={today}")

    assert res.status_code == 400

def test_get_timeslots_invalid_date(client, users):
    doctor = users["doctors"][0]

    res = client.get(f"/api/patient/timeslots?doctor_id={doctor.id}&date=15-04-2026")

    assert res.status_code == 400

def test_get_timeslots_invalid_doctor_type(client):
    res = client.get(f"/api/patient/timeslots?doctor_id=abc&date={today}")

    assert res.status_code == 400

# BOOK APPOINTMENT
def test_book_appointment_success(client, auth_header, users, schedules):
    doctor = users["doctors"][0]
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)

    res = client.post("/api/patient/appointments", json={
        "doctor_id": doctor.id,
        "schedule_id": schedule.id,
        "date": schedule.date.strftime("%Y-%m-%d"),
        "notes": "TEST NOTES"
    }, headers= auth_header)

    assert res.status_code == 200

def test_book_appointment_no_token(client):
    res = client.post("/api/patient/appointments", json={})

    assert res.status_code == 401

def test_book_appointment_wrong_role(client, doctor_token):
    res = client.post("/api/patient/appointments", json={}, headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403

def test_book_appointment_missing_doctor(client, auth_header, users, schedules):
    doctor = users["doctors"][0]
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)

    res = client.post("/api/patient/appointments", json={
        "schedule_id": schedule.id,
        "date": schedule.date.strftime("%Y-%m-%d"),
        "notes": "TEST NOTES"
    }, headers= auth_header)

    assert res.status_code == 400

def test_book_appointment_missing_schedule(client, auth_header, users, schedules):
    doctor = users["doctors"][0]
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)

    res = client.post("/api/patient/appointments", json={
        "doctor_id": doctor.id,
        "date": schedule.date.strftime("%Y-%m-%d"),
        "notes": "TEST NOTES"
    }, headers= auth_header)

    assert res.status_code == 400

def test_book_appointment_missing_date(client, auth_header, users, schedules):
    doctor = users["doctors"][0]
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)

    res = client.post("/api/patient/appointments", json={
        "doctor_id": doctor.id,
        "schedule_id": schedule.id,
        "notes": "TEST NOTES"
    }, headers= auth_header)

    assert res.status_code == 400

def test_book_appointment_past_date(client, auth_header, users, schedules):
    doctor = users["doctors"][0]
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)

    past_date = (schedule.date - timedelta(days=1)).strftime("%Y-%m-%d")

    res = client.post("/api/patient/appointments", json={
            "doctor_id": doctor.id,
            "schedule_id": schedule.id,
            "date": past_date,
            "notes": "TEST"
        }, headers=auth_header)

    assert res.status_code == 400
    assert "Cannot book past date" in res.get_json()["error"]

def test_book_appointment_not_found_schedule(client, auth_header, users):
    doctor = users["doctors"][0]
    invalid_schedule_id = 99999

    res = client.post("/api/patient/appointments", json={
        "doctor_id": doctor.id,
        "schedule_id": invalid_schedule_id,
        "date": (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "notes": "TEST NOTES"
    }, headers= auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Schedule not found" in data["error"]

def test_book_appointment_not_found_doctor(client, auth_header, schedules):
    schedule = schedules[0]
    invalid_doctor = 999999

    res = client.post("/api/patient/appointments", json={
        "doctor_id": invalid_doctor,
        "schedule_id": schedule.id,
        "date": (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "notes": "TEST NOTES"
    }, headers= auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Doctor not found" in data["error"]

def test_book_appointment_doctor_mismatch(client, auth_header, users, schedules):
    doctors = users["doctors"]
    doctor_a = doctors[0]
    doctor_b = doctors[1]

    schedule = next(s for s in schedules if s.doctor_id == doctor_a.id)

    res = client.post("/api/patient/appointments", json={
        "doctor_id": doctor_b.id,
        "schedule_id": schedule.id,
        "date": (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "notes": "TEST NOTES"
    }, headers= auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Doctor mismatch" in data["error"]

def test_book_appointment_date_mismatch(client, auth_header, users, schedules):
    doctor = users["doctors"][0]
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)

    wrong_date = (schedule.date + timedelta(days=5)).strftime("%Y-%m-%d")

    res = client.post("/api/patient/appointments", json={
            "doctor_id": doctor.id,
            "schedule_id": schedule.id,
            "date": wrong_date,
            "notes": "TEST"
        }, headers=auth_header)

    assert res.status_code == 400
    assert "Date mismatch" in res.get_json()["error"]

@pytest.mark.parametrize("status", ["BOOKED", "BLOCKED"])
def test_book_appointment_schedule_not_available(client, auth_header, users, schedules, status):
    doctor = users["doctors"][0]
    schedule = next(s for s in schedules if s.doctor_id == doctor.id)

    schedule.status = status
    db.session.commit()

    res = client.post("/api/patient/appointments", json={
            "doctor_id": doctor.id,
            "schedule_id": schedule.id,
            "date": schedule.date.strftime("%Y-%m-%d"),
            "notes": "TEST NOTES"
        }, headers=auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Slot already booked" in data["error"]

# CANCEL APPOINTMENT
def test_cancel_appointment_success(client, auth_header, appointments):
    appt = appointments[0]

    appt.status = "WAITING_EXAMINATION"
    db.session.commit()

    res = client.patch(f"/api/patient/appointments/{appt.id}/cancel", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    assert data["message"] == "Canceled successfully"

def test_cancel_appointment_update_schedule_available(client, auth_header, appointments):
    appt = appointments[0]

    appt.status = "WAITING_EXAMINATION"
    db.session.commit()

    res = client.patch(f"/api/patient/appointments/{appt.id}/cancel",headers=auth_header)

    assert res.status_code == 200

    schedule = DoctorSchedule.query.filter_by(
        doctor_id=appt.doctor_id,
        date=appt.date,
        timeslot_id=appt.timeslot_id
    ).first()

    assert schedule.status == SlotStatusEnum.AVAILABLE

def test_cancel_appointment_no_token(client, appointments):
    appt = appointments[0]

    res = client.patch(f"/api/patient/appointments/{appt.id}/cancel")

    assert res.status_code == 401

def test_cancel_appointment_wrong_role(client, doctor_token, appointments):
    appt = appointments[0]

    res = client.patch(f"/api/patient/appointments/{appt.id}/cancel", headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403
    assert "Forbidden" in res.get_json()["error"]

def test_cancel_appointment_not_found(client, auth_header):
    res = client.patch("/api/patient/appointments/999999/cancel", headers=auth_header)

    assert res.status_code == 400
    assert "Appointment not found" in res.get_json()["error"]

def test_cancel_appointment_not_owner(client, users, appointments):
    # login patient khác
    res_login = client.post("/api/auth/login", json={
            "username": users["patient_usernames"][1],
            "password": "123"
        }
    )

    token = res_login.get_json()["access_token"]

    appt = appointments[0]

    res = client.patch(f"/api/patient/appointments/{appt.id}/cancel", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400
    assert "Forbidden" in res.get_json()["error"]

@pytest.mark.parametrize("status", ["COMPLETED", "CANCELED"])
def test_cancel_appointment_invalid_status(client, auth_header, appointments, status):
    appt = appointments[0]
    appt.status = status
    db.session.commit()

    res = client.patch(f"/api/patient/appointments/{appt.id}/cancel", headers=auth_header)

    assert res.status_code == 400
    assert "Cannot cancel" in res.get_json()["error"]

def test_cancel_appointment_twice(client, auth_header, appointments):
    appt = appointments[0]
    appt.status = "WAITING_EXAMINATION"
    db.session.commit()

    first = client.patch(f"/api/patient/appointments/{appt.id}/cancel", headers=auth_header)

    assert first.status_code == 200

    second = client.patch(f"/api/patient/appointments/{appt.id}/cancel", headers=auth_header)

    assert second.status_code == 400
    assert "Cannot cancel" in second.get_json()["error"]


