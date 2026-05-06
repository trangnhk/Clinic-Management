from app.models import RoleEnum

import pytest
from unittest.mock import patch

@pytest.fixture
def patient_auth_header(patient_token):
    return {"Authorization": f"Bearer {patient_token}"}

@pytest.fixture
def doctor_auth_header(doctor_token):
    return {"Authorization": f"Bearer {doctor_token}"}

def test_get_menu_guest_no_token(client):
    res = client.get("/api/menu/")

    assert res.status_code == 200

    data = res.get_json()

    assert data["success"] is True
    assert data["role"] == "guest"
    assert isinstance(data["menus"], list)

def test_get_menu_unknown_token(client):
    res = client.get("/api/menu/", headers={"Authorization": "Bearer unknowntoken"})

    assert res.status_code == 200

    data = res.get_json()

    assert data["success"] is True
    assert data["role"] == "guest"
    assert isinstance(data["menus"], list)
    assert len(data["menus"]) >= 1

def test_get_menu_patient(client, patient_auth_header):
    res = client.get("/api/menu/", headers=patient_auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert data["success"] is True
    assert data["role"] == RoleEnum.PATIENT.value
    assert isinstance(data["menus"], list)
    assert len(data["menus"]) >= 1

def test_get_menu_doctor(client, doctor_auth_header):
    res = client.get("/api/menu/", headers=doctor_auth_header)

    assert res.status_code == 200

    data = res.get_json()

    assert data["role"] == RoleEnum.DOCTOR.value
    assert isinstance(data["menus"], list)

def test_load_menu_data_file_error():
    from app.modules.menu_bar import dao

    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            dao.load_menu_data()
