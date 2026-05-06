def test_get_doctor_detail_success(client, doctor_with_specs, doctor_reviews_data):
    doctor = doctor_reviews_data
    print(doctor)
    res = client.get(f"/api/patient/doctors/{doctor.id}")

    assert res.status_code == 200

    data = res.get_json()

    assert data["id"] == doctor.id
    assert data["name"] == doctor.user.fullname
    assert data["specialization"] == doctor.specialization.name
    assert data["total_reviews"] == len(doctor.reviews)
    assert data["rating"] == 4.0

def test_get_doctor_detail_not_found(client):
    res = client.get("/api/patient/doctors/9999")

    assert res.status_code == 404

    data = res.get_json()

    assert "Doctor not found" in data["error"]

