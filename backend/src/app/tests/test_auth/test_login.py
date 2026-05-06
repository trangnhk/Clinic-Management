import pytest
from app.db.db import db
from app.models import User

# LOGIn TEST
def test_login_success(client):
    # register
    client.post("/api/auth/register", json={
        "username": "loginuser",
        "email": "login@gmail.com",
        "password": "123456"
    })

    res = client.post("/api/auth/login", json={
        "username": "loginuser",
        "password": "123456"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data
    assert data["user"]["username"] == "loginuser"

def test_login_wrong_password(client):
    # register
    client.post("/api/auth/register", json={
        "username": "user05",
        "email": "user05@gmail.com",
        "password": "123456"
    })

    res = client.post("/api/auth/login", json={
        "username": "user05",
        "password": "wrongpass"
    })

    assert res.status_code == 401

def test_login_inactive_user(client):
    # register
    client.post("/api/auth/register", json={
        "username": "inactive",
        "email": "inactive@gmail.com",
        "password": "123456"
    })

    # set inactive
    user = User.query.filter_by(username="inactive").first()
    user.is_active = False
    db.session.commit()

    res = client.post("/api/auth/login", json={
        "username": "inactive",
        "password": "123456"
    })

    assert res.status_code == 400
    assert "inactive" in res.get_json()["error"].lower()

def test_login_user_not_exist(client):
    res = client.post("/api/auth/login", json={
        "username": "notExist",
        "password": "123456"
    })

    assert res.status_code == 401