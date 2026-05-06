import pytest

@pytest.fixture
def auth_header(patient_token):
    return {"Authorization": f"Bearer {patient_token}"}

# GET APPOINMENT
def test_get_appointments_all(client, patient_token, auth_header, users, appointments):
    res = client.get("/api/patient/appointments", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    assert isinstance(data, list)

    patient = users["patients"][0]
    expected = [a for a in appointments if a.patient_id == patient.id]

    assert len(data) == len(expected)

def test_get_appointments_wrong_role(client, doctor_token, auth_header):
    res = client.get("/api/patient/appointments", json={}, headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403

@pytest.mark.parametrize("status", ["WAITING_EXAMINATION", "PENDING_PAYMENT", "COMPLETED", "CANCELED"])
def test_get_appointments_filter_status(client, auth_header, users, appointments, status):
    res = client.get(f"/api/patient/appointments?status={status}", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    for item in data:
        assert item["status"] == status

def test_get_appointments_invalid_status(client, auth_header):
    invalid_status = "INVALID_STATUS"
    res = client.get(f"/api/patient/appointments?status={invalid_status}", headers=auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Invalid status" in data["error"]

def test_get_appointment_detail_success(client, auth_header, appointments, users):
    appt = appointments[0]

    res = client.get(f"/api/patient/appointments/{appt.id}", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    assert data["appointment_id"] == appt.id
    assert data["status"] == appt.status
    assert "patient" in data
    assert "doctor" in data
    assert "start_time" in data
    assert "end_time" in data

def test_get_appointment_detail_no_token(client, appointments):
    appt = appointments[0]

    res = client.get(f"/api/patient/appointments/{appt.id}")

    assert res.status_code == 401

def test_get_appointment_detail_wrong_role(client, doctor_token, appointments):
    appt = appointments[0]

    res = client.get(f"/api/patient/appointments/{appt.id}",
                    headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403

def test_get_appointment_detail_not_found(client, auth_header):
    res = client.get("/api/patient/appointments/999999", headers=auth_header)

    assert res.status_code == 404
    data = res.get_json()

    assert "Appointment not found" in data["error"]

def test_get_appointment_detail_not_owner(client, users, appointments):
    # login other patient
    res_login = client.post("/api/auth/login", json={
        "username": users["patient_usernames"][1],
        "password": "123"
    })

    token = res_login.get_json()["access_token"]

    appt = appointments[0]

    res = client.get(f"/api/patient/appointments/{appt.id}",
                    headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 403
    data = res.get_json()

    assert "Not your appointment" in data["error"]


# GET PROFILE
def test_get_profile_success(client, auth_header, users, appointments):
    res = client.get("/api/patient/profile", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    assert "profile" in data
    assert "medical_history" in data

    # check profile
    assert "fullname" in data["profile"]
    assert "email" in data["profile"]

    # check medical history
    history = data["medical_history"]
    assert "items" in history
    assert "pagination" in history

    assert isinstance(history["items"], list)

def test_get_profile_pagination(client, auth_header):
    res = client.get("/api/patient/profile?page=1&per_page=2", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    pagination = data["medical_history"]["pagination"]

    assert pagination["page"] == 1
    assert pagination["per_page"] == 2

def test_get_profile_invalid_page(client, auth_header):
    res = client.get("/api/patient/profile?page=0", headers=auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Invalid page" in data["error"]

def test_get_profile_invalid_per_page(client, auth_header):
    res = client.get( "/api/patient/profile?per_page=0", headers=auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Invalid per_page" in data["error"]

def test_get_profile_per_page_over_max(client, auth_header):
    res = client.get("/api/patient/profile?per_page=101", headers=auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Invalid per_page" in data["error"]

def test_get_profile_page_out_of_range(client, auth_header, appointments):
    res = client.get("/api/patient/profile?page=999", headers=auth_header)

    assert res.status_code == 400
    data = res.get_json()

    assert "Page out of range" in data["error"]

def test_get_profile_no_token(client):
    res = client.get("/api/patient/profile")

    assert res.status_code == 401

def test_get_profile_wrong_role(client, doctor_token):
    res = client.get("/api/patient/profile", headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403

def test_get_profile_patient_not_found(client, users, app):
    # tạo token giả (hoặc user không có Patient record)
    res_login = client.post("/api/auth/login", json={
        "username": "doctor0",
        "password": "123"
    })

    token = res_login.get_json()["access_token"]

    res = client.get("/api/patient/profile", headers={"Authorization": f"Bearer {token}"})

    # sẽ bị chặn bởi role trước
    assert res.status_code == 403

def test_get_profile_empty_data(client, auth_header):
    res = client.get("/api/patient/profile?page=1&per_page=2", headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    assert data["medical_history"]["items"] == []
    assert data["medical_history"]["pagination"]["total"] == 0

# UPDATE PROFILE
def test_update_profile_success_full_fields(client, auth_header):
    res = client.patch("/api/patient/profile", json={
            "fullname": "Nguyen Van A",
            "date_of_birth": "2002-05-10",
            "address": "Ho Chi Minh City",
            "phone_number": "0901234567"
        },
        headers=auth_header)

    assert res.status_code == 200
    data = res.get_json()

    assert data["fullname"] == "Nguyen Van A"
    assert data["address"] == "Ho Chi Minh City"
    assert data["date_of_birth"] == "2002-05-10"
    assert data["phone_number"] == "0901234567"
    assert "patient_id" in data
    assert "email" in data

def test_update_profile_partial_fullname(client, auth_header):
    res = client.patch("/api/patient/profile", json={"fullname": "Tran Van B"},
        headers=auth_header)

    assert res.status_code == 200
    assert res.get_json()["fullname"] == "Tran Van B"

def test_update_profile_partial_address(client, auth_header):
    res = client.patch("/api/patient/profile", json={"address": "Da Nang"},
        headers=auth_header)

    assert res.status_code == 200
    assert res.get_json()["address"] == "Da Nang"

def test_update_profile_partial_phone(client, auth_header):
    res = client.patch("/api/patient/profile", json={"phone_number": "0988888888"},
        headers=auth_header)

    assert res.status_code == 200
    assert res.get_json()["phone_number"] == "0988888888"

def test_update_profile_partial_dob(client, auth_header):
    res = client.patch("/api/patient/profile", json={"date_of_birth": "2000-01-01"},
        headers=auth_header)

    assert res.status_code == 200
    assert res.get_json()["date_of_birth"] == "2000-01-01"

def test_update_profile_two_fields(client, auth_header):
    res = client.patch("/api/patient/profile", json={
            "fullname": "Multi Update",
            "address": "Can Tho"
        }, headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()
    assert data["fullname"] == "Multi Update"
    assert data["address"] == "Can Tho"

def test_update_profile_no_token(client):
    res = client.patch("/api/patient/profile", json={"fullname": "Test"})

    assert res.status_code == 401

def test_update_profile_wrong_role(client, doctor_token):
    res = client.patch("/api/patient/profile", json={"fullname": "Doctor Edit"},
        headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403
    assert "Forbidden" in res.get_json()["error"]

def test_update_profile_no_data(client, auth_header):
    res = client.patch("/api/patient/profile", json={}, headers=auth_header)

    assert res.status_code == 400
    assert "No data provided" in res.get_json()["error"]

def test_update_profile_invalid_field_email(client, auth_header):
    res = client.patch("/api/patient/profile", json={"email": "hack@mail.com"}, headers=auth_header)

    assert res.status_code == 400
    assert "You can not update email" in res.get_json()["error"]

def test_update_profile_invalid_field_role(client, auth_header):
    res = client.patch("/api/patient/profile",json={"role": "ADMIN"}, headers=auth_header)

    assert res.status_code == 400
    assert "You can not update role" in res.get_json()["error"]

def test_update_profile_invalid_field_password(client, auth_header):
    res = client.patch("/api/patient/profile", json={"password": "123456"},headers=auth_header)

    assert res.status_code == 400

def test_update_profile_invalid_dob_string(client, auth_header):
    res = client.patch("/api/patient/profile", json={"date_of_birth": "abcxyz"}, headers=auth_header)

    assert res.status_code == 400
    assert "Invalid date" in res.get_json()["error"]

def test_update_profile_invalid_phone_string(client, auth_header):
    res = client.patch("/api/patient/profile", json={"phone_number": "abcxyz"}, headers=auth_header)

    assert res.status_code == 400
    assert "Invalid phone number" in res.get_json()["error"]