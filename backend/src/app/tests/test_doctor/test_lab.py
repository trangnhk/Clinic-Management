import pytest
from app.models import TestRequest, TestStatusEnum, AppointmentStatusEnum
from app.db.db import db

@pytest.fixture
def auth_header(doctor_token):
    return {"Authorization": f"Bearer {doctor_token}"}

# GET ALL TESTS

def test_get_all_tests_success(client, auth_header, test_data):
    res = client.get("/api/doctor/tests", headers=auth_header)
    
    assert res.status_code == 200

    data = res.get_json()

    assert len(data) == len(test_data)

def test_get_all_tests_no_token(client):
    res = client.get("/api/doctor/tests")
    
    assert res.status_code == 401

def test_get_all_tests_wrong_role(client, patient_token, test_data):
    res = client.get("/api/doctor/tests", headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]


# ADD LAB TEST
def test_add_lab_test_success(client, auth_header, in_progress_examination, test_id):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests", json={"test_id": test_id},
        headers=auth_header)
    
    assert res.status_code == 201

    assert res.json["status"] == "PENDING"

    assert in_progress_examination.appointment.status == "PENDING_RESULT"

def test_add_lab_test_no_token(client, in_progress_examination, test_id):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests", json={"test_id": test_id})

    assert res.status_code == 401

def test_add_lab_test_wrong_role(client, patient_token, in_progress_examination, test_id):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests",
        json={"test_id": test_id},
        headers={"Authorization": f"Bearer {patient_token}"}
    )

    assert res.status_code == 403
    assert "Forbidden" in res.get_json()["error"]

def test_add_lab_test_wrong_doctor(client, users, in_progress_examination, test_id):
    login = client.post("/api/auth/login", json={
        "username": users["doctor_usernames"][1],
        "password": "123"
    })

    token = login.get_json()["access_token"]

    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests",
        json={"test_id": test_id},
        headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400

    assert "Doctor mismatch" in res.get_json()["error"]

def test_add_lab_test_duplicate(client, auth_header, in_progress_examination, test_id):
    exam = in_progress_examination
    tr = TestRequest(
        appointment_id=exam.appointment_id,
        test_id=test_id
        )
    
    db.session.add(tr)
    db.session.commit()
    
    res = client.post(f"/api/doctor/examinations/{exam.id}/lab-tests",
        json={"test_id": test_id},
        headers=auth_header)
    
    assert res.status_code == 400

    assert "already exists" in res.json["error"]

def test_add_lab_test_exam_not_found(client, auth_header, test_id):
    res = client.post("/api/doctor/examinations/99999/lab-tests", json={"test_id": test_id}, headers=auth_header)

    assert res.status_code == 400

    assert "Examination not found" in res.get_json()["error"]

def test_add_lab_test_invalid_test_id(client, auth_header, in_progress_examination):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests", json={"test_id": 99999}, headers=auth_header)
    
    assert res.status_code == 400

    assert "not found" in res.get_json()["error"]

def test_add_lab_test_missing_test_id(client, auth_header, in_progress_examination):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests", json={}, headers=auth_header)

    assert res.status_code == 400

    assert "test_id is required" in res.get_json()["error"]

@pytest.mark.parametrize("appt_status", ["WAITING_EXAMINATION", "PENDING_PAYMENT", "COMPLETED", "CANCELED"])
def test_add_lab_test_wrong_appt_status(client, auth_header, in_progress_examination, test_id, appt_status):
    in_progress_examination.appointment.status = appt_status

    db.session.commit()
    
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests",
                      json={"test_id": test_id}, headers=auth_header)
    
    assert res.status_code == 400

    assert "Cannot add lab test" in res.get_json()["error"]

# GET LAB TEST
def test_get_lab_tests_success(client, auth_header, in_progress_examination, test_id):
    tr = TestRequest(
        appointment_id=in_progress_examination.appointment_id,
        test_id=test_id,
        status=TestStatusEnum.PENDING
    )
    db.session.add(tr)
    db.session.commit()

    res = client.get(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["test_id"] == test_id

def test_get_lab_tests_empty(client, auth_header, in_progress_examination):
    res = client.get(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests", headers=auth_header)

    assert res.status_code == 200

    assert res.get_json() == []

def test_get_lab_tests_exam_not_found(client, auth_header):
    res = client.get("/api/doctor/examinations/99999/lab-tests", headers=auth_header)

    assert res.status_code == 400

    assert "Examination not found" in res.get_json()["error"]

def test_get_lab_tests_wrong_doctor(client, users, in_progress_examination):
    login = client.post("/api/auth/login", json={
        "username": users["doctor_usernames"][1],
        "password": "123"
    })

    token = login.get_json()["access_token"]

    res = client.get(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests",
        headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400

    assert "Doctor mismatch" in res.get_json()["error"]

def test_get_lab_tests_wrong_role(client, patient_token, in_progress_examination):

    res = client.get(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests",
        headers={"Authorization": f"Bearer {patient_token}"})

    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_get_lab_tests_no_token(client, in_progress_examination):
    res = client.get(f"/api/doctor/examinations/{in_progress_examination.id}/lab-tests")

    assert res.status_code == 401

# DELETE LAB TEST
def test_delete_lab_test_success(client, auth_header, in_progress_examination, test_id):
    tr = TestRequest(
        appointment_id=in_progress_examination.appointment_id,
        test_id=test_id,
        status=TestStatusEnum.PENDING
    )
    db.session.add(tr)
    db.session.commit()

    res = client.delete(f"/api/doctor/lab-tests/{tr.id}", headers=auth_header)

    assert res.status_code == 200
    assert "Deleted" in res.get_json()["message"]

def test_delete_lab_test_wrong_doctor(client, users, in_progress_examination, test_id):
    tr = TestRequest(
        appointment_id=in_progress_examination.appointment_id,
        test_id=test_id,
        status=TestStatusEnum.PENDING
    )
    db.session.add(tr)
    db.session.commit()

    login = client.post("/api/auth/login", json={
        "username": users["doctor_usernames"][1],
        "password": "123"
    })

    token = login.get_json()["access_token"]

    res = client.delete(f"/api/doctor/lab-tests/{tr.id}",
        headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400
    assert "Doctor mismatch" in res.get_json()["error"]

def test_delete_lab_test_wrong_role(client, patient_token, in_progress_test_request):
    res = client.delete(f"/api/doctor/lab-tests/{in_progress_test_request.id}",
        headers={"Authorization": f"Bearer {patient_token}"})

    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_delete_lab_test_no_token(client, in_progress_test_request):
    res = client.delete(f"/api/doctor/lab-tests/{in_progress_test_request.id}")

    assert res.status_code == 401

def test_delete_lab_test_not_found(client, auth_header):
    res = client.delete("/api/doctor/lab-tests/99999", headers=auth_header)

    assert res.status_code == 400

    assert "Test request not found" in res.get_json()["error"]

@pytest.mark.parametrize("status", ["IN_PROGRESS", "DONE"])
def test_delete_lab_test_not_pending(client, auth_header, in_progress_test_request, status):
    tr = in_progress_test_request
    tr.status = status

    db.session.commit()
    
    res = client.delete(f"/api/doctor/lab-tests/{in_progress_test_request.id}",
        headers=auth_header)
    
    assert res.status_code == 400

    assert "Cannot delete" in res.json["error"]
