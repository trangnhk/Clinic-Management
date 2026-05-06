import pytest
from app.db.db import db
from app.models import User, Patient, Doctor

# REGISTER TEST
def test_register_success(client):
    res = client.post("/api/auth/register", json={
        "username": "user01",
        "email": "user01@gmail.com",
        "password": "123456"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert data["username"] == "user01"

def test_register_missing_emails(client):
    res = client.post("/api/auth/register", json={
        "username": "user01",
        "password": "123456"
    })

    assert res.status_code == 400
    assert "error" in res.get_json()

def test_register_missing_password(client):
    res = client.post("/api/auth/register", json={
        "username": "user01",
        "email": "user01@gmail.com"
    })

    assert res.status_code == 400
    assert "error" in res.get_json()

def test_register_missing_username(client):
    res = client.post("/api/auth/register", json={
        "email": "user01@gmail.com",
        "password": "123456"
    })

    assert res.status_code == 400
    assert "error" in res.get_json()

def test_register_with_invalid_email(client):
    res = client.post("/api/auth/register", json={
        "username": "invalidEmail",
        "email": "invalidgmail.com",
        "password": "123456"
    })

    assert res.status_code == 400
    assert "Invalid email" in res.get_json()["error"]

def test_register_duplicate_username(client):
    # register one user
    client.post("/api/auth/register", json={
        "username": "dupuser",
        "email": "dup@gmail.com",
        "password": "123456"
    })

    # register duplicate user
    res = client.post("/api/auth/register", json={
        "username": "dupuser",
        "email": "new@gmail.com",
        "password": "123456"
    })

    assert res.status_code == 400
    assert "Username already exists" in res.get_json()["error"]

def test_register_duplicate_email(client):
    # register one user
    client.post("/api/auth/register", json={
        "username": "user03",
        "email": "same@gmail.com",
        "password": "123456"
    })

    # register duplicate user
    res = client.post("/api/auth/register", json={
        "username": "user04",
        "email": "same@gmail.com",
        "password": "123456"
    })

    assert res.status_code == 400
    assert "Email already exists" in res.get_json()["error"]

def test_register_user_and_create_patient_profile(client):
    # register one user
    res = client.post("/api/auth/register", json={
        "username": "user_profile",
        "email": "use_profiler@gmail.com",
        "password": "123456"
    })

    assert res.status_code == 200

    user = User.query.filter_by(username="user_profile").first()
    patient = Patient.query.filter_by(user_id=user.id).first()

    assert user is not None
    assert patient is not None

def test_event_with_invalid_role(app):
    user = User(
        username="admin1",
        email="admin@gmail.com",
        password_hash="123",
        role="ADMIN"
    )
    db.session.add(user)
    db.session.commit()

    patient = Patient.query.filter_by(user_id=user.id).first()
    doctor = Doctor.query.filter_by(user_id=user.id).first()

    assert patient is None
    assert doctor is None
