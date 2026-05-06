import pytest

@pytest.fixture
def auth_header(doctor_token):
    return {"Authorization": f"Bearer {doctor_token}"}

# GET PROFILE
def test_get_profile_success(client, auth_header, doctor_reviews_data):
    res = client.get("/api/doctor/profile", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert "doctor_id" in data
    assert "fullname" in data
    assert res.get_json()["rating"] == 4.0
    assert "experience_years" in data

def test_get_profile_forbidden(client, patient_token):
    res = client.get("/api/doctor/profile", headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403

def test_get_profile_no_token(client):
    res = client.get("/api/doctor/profile")
    
    assert res.status_code == 401


# UPDATE PROFILE
def test_patch_profile_multi_update_success(client, auth_header):
    res = client.patch("/api/doctor/profile", json={
        "fullname": "Bs. Nguyễn Văn A", 
        "experience_years": 5
        }, headers=auth_header)
    
    assert res.status_code == 200

    assert res.get_json()["fullname"] == "Bs. Nguyễn Văn A"

def test_patch_profile_partial_update_description(client, auth_header):
    res = client.patch("/api/doctor/profile", json={
        "description": "Chuyên gia tim mạch"
        }, headers=auth_header)
    
    assert res.status_code == 200
    
    assert res.get_json()["description"] == "Chuyên gia tim mạch"

def test_patch_profile_partial_update_phone(client, auth_header):
    res = client.patch("/api/doctor/profile", json={
        "phone_number": "0999999999"
        }, headers=auth_header)
    
    assert res.status_code == 200
    
    assert res.get_json()["phone_number"] == "0999999999"

def test_patch_profile_empty_body(client, auth_header):
    res = client.patch("/api/doctor/profile", json={}, headers=auth_header)
    
    assert res.status_code == 200

    data = res.get_json()

    assert "fullname" in data
    assert "doctor_id" in data

def test_patch_profile_forbidden(client, patient_token):
    res = client.patch("/api/doctor/profile", json={
        "fullname": "x"
        }, headers={"Authorization": f"Bearer {patient_token}"})
    
    assert res.status_code == 403

def test_patch_profile_no_token(client):
    res = client.patch("/api/doctor/profile", json={"fullname": "x"})

    assert res.status_code == 401

@pytest.mark.parametrize("phone", ["abc", "123", "01234567890", "09abc99999", "1234567890"])
def test_patch_profile_invalid_phone(client, auth_header, phone):
    res = client.patch("/api/doctor/profile", json={
        "phone_number": phone
        }, headers=auth_header)

    assert res.status_code == 400

    assert "Invalid phone number" in res.get_json()["error"]

def test_patch_profile_invalid_years(client, auth_header):
    res = client.patch("/api/doctor/profile", json={
        "experience_years": -2
    }, headers=auth_header)

    assert res.status_code == 400

    assert "Invalid experience years" in res.get_json()["error"]


# GET CALENDAR
def test_get_calendar_success(client, auth_header):
    res = client.get("/api/doctor/profile/calendar?month=5&year=2026", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert "days_with_schedule" in data
    assert "days_with_appointments" in data
    assert "calendar" in data
    assert data["month"] == 5
    assert data["year"] == 2026

def test_get_calendar_forbidden(client, patient_token):
    res = client.get("/api/doctor/profile/calendar?month=5&year=2026",
        headers={"Authorization": f"Bearer {patient_token}"})

    assert res.status_code == 403
    assert "Forbidden" in res.get_json()["error"]

def test_get_calendar_no_token(client):
    res = client.get("/api/doctor/profile/calendar?month=5&year=2026")

    assert res.status_code == 401

def test_get_calendar_missing_month(client, auth_header):
    res = client.get("/api/doctor/profile/calendar?year=2026", headers=auth_header)

    assert res.status_code == 400

def test_get_calendar_missing_year(client, auth_header):
    res = client.get("/api/doctor/profile/calendar?month=5", headers=auth_header)

    assert res.status_code == 400

@pytest.mark.parametrize("month", [-1, 13])
def test_get_calendar_invalid_month(client, auth_header, month):
    res = client.get(f"/api/doctor/profile/calendar?month={month}&year=2026", headers=auth_header)

    assert res.status_code == 400

    assert "Invalid month" in res.get_json()["error"]

@pytest.mark.parametrize("year", [2025, 2101])
def test_get_calendar_invalid_year(client, auth_header, year):
    res = client.get(f"/api/doctor/profile/calendar?month=5&year={year}", headers=auth_header)

    assert res.status_code == 400

    assert "Invalid year" in res.get_json()["error"]

def test_get_calendar_has_day_items(client, auth_header, schedules, appointments):
    res = client.get("/api/doctor/profile/calendar?month=5&year=2026", headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    day_item = list(data["calendar"].values())[0]
    assert "has_schedule" in day_item
    assert "appointments" in day_item
    assert isinstance(data["days_with_schedule"], list)



