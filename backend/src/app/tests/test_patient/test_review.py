import pytest
from app.models import Review

@pytest.fixture
def auth_header(patient_token):
    return {"Authorization": f"Bearer {patient_token}"}

# CREATE REVIEW
def test_create_review_success(client, auth_header, completed_appointment):
    appt = completed_appointment

    res = client.post(f"/api/patient/appointments/{appt.id}/review", json={
            "rating": 5,
            "comment": "Very good doctor"
        }, headers=auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert "review_id" in data
    assert data["message"] == "Review success"

def test_create_review_no_token(client, completed_appointment):
    res = client.post(f"/api/patient/appointments/{completed_appointment.id}/review", json={"rating": 5})

    assert res.status_code == 401

def test_create_review_wrong_role(client, doctor_token, completed_appointment):

    res = client.post(f"/api/patient/appointments/{completed_appointment.id}/review", json={"rating": 5},
        headers={"Authorization": f"Bearer {doctor_token}"})

    assert res.status_code == 403
    assert "Forbidden" in res.get_json()["error"]

def test_create_review_not_owner(client, users, completed_appointment):
    login = client.post("/api/auth/login", json={
            "username": users["patient_usernames"][1],
            "password": "123"
        }
    )

    token = login.get_json()["access_token"]

    res = client.post(f"/api/patient/appointments/{completed_appointment.id}/review", json={"rating": 5},
        headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 403
    assert "Forbidden" in res.get_json()["error"]

def test_create_review_appointment_not_found( client, auth_header):
    res = client.post("/api/patient/appointments/99999/review", json={"rating": 5}, headers=auth_header)

    assert res.status_code == 404
    assert "Appointment no found" in res.get_json()["error"]

def test_create_review_not_completed(client, auth_header, paid_appointment):
    appt = paid_appointment

    res = client.post(f"/api/patient/appointments/{appt.id}/review", json={"rating": 5}, headers=auth_header)

    assert res.status_code == 400
    assert "Only completed appointment can review" in res.get_json()["error"]

def test_create_review_already_reviewed(client, auth_header, completed_appointment):
    appt = completed_appointment

    client.post(f"/api/patient/appointments/{appt.id}/review", json={"rating": 5}, headers=auth_header)

    res = client.post(f"/api/patient/appointments/{appt.id}/review", json={"rating": 4}, headers=auth_header)

    assert res.status_code == 400
    assert "Already reviewed" in res.get_json()["error"]

@pytest.mark.parametrize("rating", [1, 2, 3, 4, 5])
def test_create_review_valid_rating_range(client, auth_header, completed_appointment, rating):
    appt = completed_appointment

    res = client.post(f"/api/patient/appointments/{appt.id}/review", json={"rating": rating}, headers=auth_header)

    assert res.status_code == 200

@pytest.mark.parametrize("rating", [0, -1, 6, 10])
def test_create_review_invalid_rating_range(client, auth_header, completed_appointment, rating):
    appt = completed_appointment

    res = client.post(f"/api/patient/appointments/{appt.id}/review", json={"rating": rating},headers=auth_header)

    assert res.status_code == 400

    assert "Invalid rating" in res.get_json()["error"]

def test_create_review_missing_rating(client, auth_header, completed_appointment):
    res = client.post(
        f"/api/patient/appointments/{completed_appointment.id}/review", json={"comment": "Good"}, headers=auth_header)

    assert res.status_code == 400

def test_create_review_correct_doctor_and_patient(client, auth_header, completed_appointment):
    appt = completed_appointment

    client.post(f"/api/patient/appointments/{appt.id}/review", json={"rating": 5}, headers=auth_header)

    review = Review.query.filter_by(appointment_id=appt.id).first()

    assert review.doctor_id == appt.doctor_id
    assert review.patient_id == appt.patient_id

# GET DOCTOR REVIEW
def test_get_doctor_reviews_success(client, doctor_reviews_data):
    doctor = doctor_reviews_data

    res = client.get(f"/api/patient/doctors/{doctor.id}/reviews")

    assert res.status_code == 200

    data = res.get_json()

    assert "doctor_id" in data
    assert "average_rating" in data
    assert "total_reviews" in data
    assert "rating_breakdown" in data
    assert "reviews" in data

def test_get_doctor_reviews_total_reviews(client, doctor_reviews_data):
    doctor = doctor_reviews_data

    res = client.get(f"/api/patient/doctors/{doctor.id}/reviews")

    assert res.status_code == 200
    assert res.get_json()["total_reviews"] == 3

def test_get_doctor_reviews_average_rating(client, doctor_reviews_data):
    doctor = doctor_reviews_data

    res = client.get(f"/api/patient/doctors/{doctor.id}/reviews")

    assert res.status_code == 200

    # (5 + 4 + 3) / 3 = 4.0
    assert res.get_json()["average_rating"] == 4.0

def test_get_doctor_reviews_breakdown(client, doctor_reviews_data):
    doctor = doctor_reviews_data

    res = client.get(f"/api/patient/doctors/{doctor.id}/reviews")

    data = res.get_json()["rating_breakdown"]

    assert data["1"] == 0
    assert data["2"] == 0
    assert data["3"] == 1
    assert data["4"] == 1
    assert data["5"] == 1

def test_get_doctor_reviews_sorted_latest_first(client, doctor_reviews_data):
    doctor = doctor_reviews_data

    res = client.get(f"/api/patient/doctors/{doctor.id}/reviews")

    reviews = res.get_json()["reviews"]

    assert reviews[0]["rating"] == 3
    assert reviews[1]["rating"] == 4
    assert reviews[2]["rating"] == 5

def test_get_doctor_reviews_not_found(client):
    res = client.get("/api/patient/doctors/9999/reviews")

    assert res.status_code == 404
    assert "Doctor not found" in res.get_json()["error"]

def test_get_doctor_reviews_no_review(client, users):
    doctor = users["doctors"][1]

    res = client.get(f"/api/patient/doctors/{doctor.id}/reviews")

    assert res.status_code == 200

    data = res.get_json()

    assert data["doctor_id"] == doctor.id
    assert data["average_rating"] == 0
    assert data["total_reviews"] == 0
    assert data["reviews"] == []

    assert data["rating_breakdown"]["1"] == 0
    assert data["rating_breakdown"]["2"] == 0
    assert data["rating_breakdown"]["3"] == 0
    assert data["rating_breakdown"]["4"] == 0
    assert data["rating_breakdown"]["5"] == 0

def test_get_doctor_reviews_comment_content(client, doctor_reviews_data):
    doctor = doctor_reviews_data

    res = client.get(f"/api/patient/doctors/{doctor.id}/reviews")

    comments = [r["comment"] for r in res.get_json()["reviews"]]

    assert "Excellent" in comments
    assert "Very good" in comments
    assert "Normal" in comments






