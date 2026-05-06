import pytest

def test_register_sql_injection(client):
    res = client.post("/api/auth/register", json={
        "username": "' OR 1=1 --",
        "email": "hack@gmail.com",
        "password": "123456"
    })

    # hệ thống không crash
    assert res.status_code in [200, 400]


def test_login_sql_injection(client):
    res = client.post("/api/auth/login", json={
        "username": "' OR 1=1 --",
        "password": "123456"
    })

    assert res.status_code == 401