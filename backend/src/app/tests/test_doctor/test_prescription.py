import pytest
from app.models import PrescriptionDetail, Prescription
from app.db.db import db

@pytest.fixture
def auth_header(doctor_token):
    return {"Authorization": f"Bearer {doctor_token}"}

# GET ALL MEDICINES]
def test_get_all_medicines_success(client, auth_header, medicine_data):
    res = client.get("/api/doctor/medicines", headers=auth_header)
    
    assert res.status_code == 200

    data = res.get_json()

    assert len(data) == len(medicine_data)

def test_get_all_medicines_no_token(client):
    res = client.get("/api/doctor/medicines")
    
    assert res.status_code == 401

def test_get_all_medicines_wrong_role(client, patient_token, medicine_data):
    res = client.get("/api/doctor/medicines", headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

# ADD PRESCRIPTION DETAIL
def test_add_prescription_success(client, auth_header, in_progress_examination, medicine_data):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions", json={
        "medicine_id": medicine_data[0].id,
        "quantity": 2, 
        "dosage": "2 viên/ngày",
        "instruction": "Uống sau ăn"
        }, headers=auth_header)
    
    assert res.status_code == 201

    data = res.get_json()

    assert data["quantity"] == 2
    assert data["medicine_id"] == medicine_data[0].id
    assert "prescription_id" in data
    assert "detail_id" in data

def test_add_prescription_create_new_prescription(client, auth_header, in_progress_examination, medicine_data):
    assert in_progress_examination.prescription is None

    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions",
        json={
            "medicine_id": medicine_data[0].id,
            "quantity": 1
        }, headers=auth_header)

    assert res.status_code == 201

    db.session.expire_all()
    pres = Prescription.query.filter_by(examination_id=in_progress_examination.id).first()

    assert pres is not None
    assert len(pres.details) == 1

def test_add_prescription_reuse_existing_prescription(client, auth_header, prescription_detail, medicine_data):
    exam_id = prescription_detail.examination_id
    old_pres_id = prescription_detail.id

    res = client.post(f"/api/doctor/examinations/{exam_id}/prescriptions",
        json={
            "medicine_id": medicine_data[1].id,
            "quantity": 3
        }, headers=auth_header)

    assert res.status_code == 201
    assert res.get_json()["prescription_id"] == old_pres_id

def test_add_prescription_no_token(client, in_progress_examination):
    res = client.post( f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions",
        json={
            "medicine_id": 1, 
            "quantity": 1})

    assert res.status_code == 401

def test_add_prescription_wrong_role(client, patient_token, in_progress_examination):
    res = client.post(
        f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions",
        json={
            "medicine_id": 1, 
            "quantity": 1
            }, headers={"Authorization": f"Bearer {patient_token}"})

    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_add_prescription_wrong_doctor(client, users, in_progress_examination, medicine_data):
    login = client.post("/api/auth/login", json={
        "username": users["doctor_usernames"][1],
        "password": "123"
    })

    token = login.get_json()["access_token"]

    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions",
        json={
            "medicine_id": medicine_data[0].id,
            "quantity": 1
        }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400

    assert "Doctor mismatch" in res.get_json()["error"]

def test_add_prescription_request_body_required(client, auth_header, in_progress_examination):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions", json={}, headers=auth_header)

    assert res.status_code == 400
    assert "Request body is required" in res.get_json()["error"]

@pytest.mark.parametrize("field", ["medicine_id", "quantity"])
def test_add_prescription_missing_fields(client, auth_header, in_progress_examination, field):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions", json={
        f"{field}": 1
        }, headers=auth_header)
    
    assert res.status_code == 400

    assert "medicine_id and quantity are required" in res.get_json()["error"]

def test_add_prescription_medicine_not_found(client, auth_header, in_progress_examination):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions",json={
        "medicine_id": 99999, 
        "quantity": 1
        }, headers=auth_header)
    
    assert res.status_code == 400

    assert "not found" in res.json["error"]

def test_add_prescription_exam_not_found(client, auth_header, medicine_data):
    res = client.post("/api/doctor/examinations/99999/prescriptions",
        json={
            "medicine_id": medicine_data[0].id,
            "quantity": 1
        }, headers=auth_header)

    assert res.status_code == 400

    assert "Examination not found" in res.get_json()["error"]

@pytest.mark.parametrize("field", [-1, "quantity", "2"])
def test_add_prescription_invalid_quantity(client, auth_header, in_progress_examination, medicine_data, field):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions", json={
        "medicine_id": medicine_data[0].id,
        "quantity": field
        }, headers=auth_header)
    
    assert res.status_code == 400

def test_add_prescription_invalid_medicine_type(client, auth_header, in_progress_examination):
    res = client.post(f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions",
        json={
            "medicine_id": "abc",
            "quantity": 1
        }, headers=auth_header)

    assert res.status_code == 400
    assert "interger" in res.get_json()["error"]

@pytest.mark.parametrize("status", ["WAITING_EXAMINATION", "PENDING_PAYMENT", "COMPLETED", "CANCELED"])
def test_add_prescription_wrong_status(client, auth_header, in_progress_examination, medicine_data, status):
    appt = in_progress_examination.appointment
    appt.status = status
    db.session.commit()

    res = client.post(
        f"/api/doctor/examinations/{in_progress_examination.id}/prescriptions",
        json={
            "medicine_id": medicine_data[0].id,
            "quantity": 1
        }, headers=auth_header)

    assert res.status_code == 400

    assert "Cannot update appointment" in res.get_json()["error"]


# DELETE PRESCRIPTION DETAIL
def test_delete_prescription_detail_success(client, auth_header, prescription_detail_id):
    res = client.delete(f"/api/doctor/prescriptions/{prescription_detail_id}", headers=auth_header)

    assert res.status_code == 200

    assert "Deleted successfully" in res.get_json()["message"]

def test_delete_prescription_detail_no_token(client, prescription_detail_id):
    res = client.delete(f"/api/doctor/prescriptions/{prescription_detail_id}")

    assert res.status_code == 401

def test_delete_prescription_detail_wrong_role(client, users, prescription_detail_id):
    other_user = users["patient_usernames"][0]

    doctor_login = client.post("/api/auth/login", json={
        "username": other_user,
        "password": "123"
    })

    token = doctor_login.get_json()["access_token"]

    res = client.delete(f"/api/doctor/prescriptions/{prescription_detail_id}", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 403

    assert "Forbidden" in res.get_json()["error"]

def test_delete_prescription_detail_wrong_doctor(client, users, prescription_detail_id):
    other_user = users["doctor_usernames"][1]

    doctor_login = client.post("/api/auth/login", json={
        "username": other_user,
        "password": "123"
    })

    token = doctor_login.get_json()["access_token"]

    res = client.delete(f"/api/doctor/prescriptions/{prescription_detail_id}", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 400

    assert "Forbidden" in res.get_json()["error"]

def test_delete_prescription_detail_not_found(client, auth_header, prescription_detail_id):
    res = client.delete(f"/api/doctor/prescriptions/99999", headers=auth_header)

    assert res.status_code == 400

    assert "Prescription detail not found" in res.get_json()["error"]

def test_delete_prescription_completed_exam_block(client, auth_header, prescription_detail):
    appt = prescription_detail.examination.appointment
    appt.status = "COMPLETED"
    db.session.commit()

    detail = PrescriptionDetail.query.filter_by(prescription_id=prescription_detail.id).first()

    res = client.delete(f"/api/doctor/prescriptions/{detail.id}", headers=auth_header)

    assert res.status_code == 400
    assert "Cannot modify a completed examination" in res.get_json()["error"]

def test_delete_prescription_after_delete_not_found(client, auth_header, prescription_detail_id):
    client.delete(f"/api/doctor/prescriptions/{prescription_detail_id}", headers=auth_header)

    res = client.delete(f"/api/doctor/prescriptions/{prescription_detail_id}", headers=auth_header)

    assert res.status_code == 400
    assert "Prescription detail not found" in res.get_json()["error"]








