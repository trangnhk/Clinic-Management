import pytest
from app.app import create_app
from app.db.db import db
from app.models import (
    Specialization, User, Patient, Doctor, Review, TimeSlot,
    DoctorSchedule, Payment, Appointment, Examination,
    Medicine, Prescription, PrescriptionDetail,
    Test, TestRequest, TestStatusEnum
)
from datetime import datetime, timedelta, date
from app.modules.user.dao import generate_password_hash


#  APP / CLIENT 
@pytest.fixture(scope="function")
def app():
    app = create_app("testing")
    app.config.update({"TESTING": True})
    with app.app_context():
        db.session.remove()
        db.session.rollback()
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.session.rollback()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


#  USERS 
@pytest.fixture
def users(app):
    patients_users = []
    doctors_users = []

    for i in range(3):
        user = User(
            username=f"patient{i}",
            email=f"patient{i}@mail.com",
            password_hash=generate_password_hash("123"),
            role="PATIENT",
        )
        db.session.add(user)
        patients_users.append(user)
    db.session.flush()

    patients = [Patient.query.filter_by(user_id=u.id).first() for u in patients_users]

    for i in range(3):
        user = User(
            username=f"doctor{i}",
            email=f"doctor{i}@mail.com",
            password_hash=generate_password_hash("123"),
            role="DOCTOR",
            fullname=f"Dr {i}",
        )
        db.session.add(user)
        doctors_users.append(user)
    db.session.flush()

    doctors = [Doctor.query.filter_by(user_id=u.id).first() for u in doctors_users]
    db.session.commit()

    return {
        "patients": patients,
        "doctors": doctors,
        "patient_usernames": [p.user.username for p in patients],
        "doctor_usernames": [d.user.username for d in doctors],
    }


#  SPECIALIZATIONS 
@pytest.fixture
def specializations(app):
    specs = []
    for name in ["Cardiology", "Dermatology", "Neurology"]:
        spec = Specialization(name=name)
        db.session.add(spec)
        specs.append(spec)
    db.session.commit()
    return specs


#  DOCTOR -> SPECIALIZATION 
@pytest.fixture
def doctor_with_specs(app, users, specializations):
    doctors = users["doctors"]
    for i, doctor in enumerate(doctors):
        doctor.specialization_id = specializations[i % len(specializations)].id
    db.session.commit()
    return doctors


#  TIMESLOTS 
@pytest.fixture
def timeslots(app):
    slots = []
    base = datetime.strptime("08:00", "%H:%M")
    for i in range(6):
        start = (base + timedelta(minutes=30 * i)).time()
        end = (datetime.combine(datetime.today(), start) + timedelta(minutes=30)).time()
        slot = TimeSlot(start_time=start, end_time=end)
        db.session.add(slot)
        slots.append(slot)
    db.session.commit()
    return slots


#  SCHEDULES 
@pytest.fixture
def schedules(app, doctor_with_specs, timeslots):
    schedules = []
    for doc in doctor_with_specs:
        for i in range(3):
            schedule = DoctorSchedule(
                doctor_id=doc.id,
                date=datetime.now().date() + timedelta(days=i),
                timeslot_id=timeslots[i].id,
                status="AVAILABLE",
            )
            db.session.add(schedule)
            schedules.append(schedule)
    db.session.commit()
    return schedules


#  APPOINTMENTS (multi-status) 
@pytest.fixture
def appointments(app, users, doctor_with_specs, schedules):
    patients = users["patients"]
    appts = []
    statuses = ["PENDING_PAYMENT", "WAITING_EXAMINATION", "COMPLETED", "CANCELED"]
    for i, schedule in enumerate(schedules):
        appt = Appointment(
            patient_id=patients[i % len(patients)].id,
            doctor_id=schedule.doctor_id,
            timeslot_id=schedule.timeslot_id,
            date=schedule.date,          
            status=statuses[i % len(statuses)],
            payment_status="PENDING",
        )
        db.session.add(appt)
        appts.append(appt)
    db.session.commit()
    return appts


@pytest.fixture
def doctor_appointments(app, users, doctor_with_specs, timeslots):
    doctor = users["doctors"][0]
    patients = users["patients"]
    appts = []
    statuses = [
        "WAITING_EXAMINATION",
        "IN_PROGRESS",
        "PENDING_RESULT",
        "COMPLETED",
    ]
    for i, status in enumerate(statuses):
        appt = Appointment(
            patient_id=patients[i % len(patients)].id,
            doctor_id=doctor.id,
            timeslot_id=timeslots[i].id,
            date=datetime.now().date(),
            status=status,
            payment_status="PAID",
        )
        db.session.add(appt)
        appts.append(appt)
    db.session.commit()
    return appts

#  WAITING APPOINTMENT (for doctor[0]) 
@pytest.fixture
def waiting_appointment(app, users, doctor_with_specs, timeslots):
    doctor = users["doctors"][0]
    patient = users["patients"][0]
    appt = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        timeslot_id=timeslots[0].id,
        date=datetime.now().date(),
        status="WAITING_EXAMINATION",
        payment_status="PAID",
    )
    db.session.add(appt)
    db.session.commit()
    return appt

# PENDING PAYMENT APPOINTMENT
@pytest.fixture
def pending_payment_appointment(app, users, doctor_with_specs, timeslots):
    patient = users["patients"][0]
    doctor = users["doctors"][0]
    appt = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        timeslot_id=timeslots[2].id,
        date=datetime.now().date() + timedelta(days=1),
        status="PENDING_PAYMENT",
        payment_status="PENDING",
    )
    db.session.add(appt)
    db.session.commit()

    # Tạo schedule tương ứng để auto_cancel có thể release
    schedule = DoctorSchedule(
        doctor_id=doctor.id,
        date=appt.date,
        timeslot_id=timeslots[2].id,
        status="BOOKED",
    )
    db.session.add(schedule)
    db.session.commit()
    return appt

#  IN-PROGRESS APPOINTMENT (no exam) 
@pytest.fixture
def in_progress_appointment(app, waiting_appointment):
    appt = waiting_appointment
    appt.status = "IN_PROGRESS"
    db.session.commit()
    return appt

#  COMPLETED APPOINTMENT 
@pytest.fixture
def completed_appointment(app, users, doctor_with_specs, timeslots):
    doctor = users["doctors"][0]
    patient = users["patients"][0]
    appt = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        timeslot_id=timeslots[0].id,
        date=datetime.now().date(),
        status="COMPLETED",
        payment_status="PAID",
    )
    db.session.add(appt)
    db.session.commit()
    return appt

# PAID APPOINTMENT
@pytest.fixture
def paid_appointment(app, users, doctor_with_specs, timeslots):
    patient = users["patients"][0]
    doctor = users["doctors"][0]
    appt = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        timeslot_id=timeslots[1].id,
        date=datetime.now().date(),
        status="WAITING_EXAMINATION",
        payment_status="PAID",
    )
    db.session.add(appt)
    db.session.commit()
    return appt

# PAYMENT FOR COMPLETED APPOINTMENT
@pytest.fixture
def payment_completed(app, completed_appointment):
    p1 = Payment(
        appointment_id=completed_appointment.id,
        payment_type="DEPOSIT",
        amount=10000,
        status="PAID",
        paid_at=datetime.now()
    )
    p2 = Payment(
        appointment_id=completed_appointment.id,
        payment_type="MEDICINE",
        amount=35000,
        status="PAID",
        paid_at=datetime.now()
    )
    p3 = Payment(
        appointment_id=completed_appointment.id,
        payment_type="FINAL",
        amount=50000,
        status="PAID",
        paid_at=datetime.now()
    )
    db.session.add_all([p1, p2, p3])
    db.session.commit()
    return [p1, p2, p3]

#  IN-PROGRESS EXAMINATION (exam exists, appt IN_PROGRESS) 
@pytest.fixture
def in_progress_examination(app, waiting_appointment):
    appt = waiting_appointment
    exam = Examination(appointment_id=appt.id, diagnosis="Test in progress examination")
    db.session.add(exam)
    appt.status = "IN_PROGRESS"
    db.session.commit()
    return exam

@pytest.fixture
def completed_examination(app, completed_appointment):
    appt = completed_appointment
    exam = Examination(appointment_id=appt.id, diagnosis="Test Examination")
    db.session.add(exam)
    db.session.commit()
    return exam


#  MEDICINE 
@pytest.fixture
def medicine_data(app):
    med1 = Medicine(name="Paracetamol", price=10000)
    med2 = Medicine(name="Vitamin C", price=15000)
    db.session.add_all([med1, med2])
    db.session.commit()
    return [med1, med2]


#  PRESCRIPTION + DETAILS 
@pytest.fixture
def prescription_detail(app, in_progress_examination, medicine_data):
    pres = Prescription(examination_id=in_progress_examination.id)
    db.session.add(pres)
    db.session.flush()
    d1 = PrescriptionDetail(
        prescription_id=pres.id, medicine_id=medicine_data[0].id,
        quantity=2, dosage="2/day", instruction="After meal",
    )
    d2 = PrescriptionDetail(
        prescription_id=pres.id, medicine_id=medicine_data[1].id,
        quantity=1, dosage="1/day", instruction="Morning",
    )
    db.session.add_all([d1, d2])
    db.session.commit()
    return pres


@pytest.fixture
def prescription_detail_id(app, prescription_detail):
    detail = PrescriptionDetail.query.filter_by(prescription_id=prescription_detail.id).first()
    return detail.id

@pytest.fixture
def prescription_with_completed_exam(app, completed_examination, medicine_data):
    pres = Prescription(examination_id=completed_examination.id)
    db.session.add(pres)
    db.session.flush()
    d1 = PrescriptionDetail(
        prescription_id=pres.id, medicine_id=medicine_data[0].id,
        quantity=2, dosage="2/day", instruction="After meal",
    )
    d2 = PrescriptionDetail(
        prescription_id=pres.id, medicine_id=medicine_data[1].id,
        quantity=1, dosage="1/day", instruction="Morning",
    )
    db.session.add_all([d1, d2])
    db.session.commit()
    return pres


#  LAB TESTS 
@pytest.fixture
def test_data(app):
    t1 = Test(name="Xét nghiệm máu", price=50000, description="Công thức máu toàn phần")
    t2 = Test(name="Chụp X-quang", price=100000, description="X-quang ngực thẳng")
    db.session.add_all([t1, t2])
    db.session.commit()
    return [t1, t2]


@pytest.fixture
def test_id(app, test_data):
    return test_data[0].id


@pytest.fixture
def in_progress_test_request(app, in_progress_examination, test_data):
    exam = in_progress_examination
    tr = TestRequest(
        appointment_id=exam.appointment_id,
        test_id=test_data[0].id,
        status=TestStatusEnum.IN_PROGRESS,
    )
    db.session.add(tr)
    db.session.commit()
    return tr


#  DOCTOR REVIEWS 
@pytest.fixture
def doctor_reviews_data(app, users, completed_appointment):
    doctor = users["doctors"][0]
    patients = users["patients"]
    appt2 = Appointment(
        patient_id=patients[1].id, doctor_id=doctor.id,
        timeslot_id=completed_appointment.timeslot_id,
        date=completed_appointment.date, status="COMPLETED", payment_status="PAID",
    )
    appt3 = Appointment(
        patient_id=patients[2].id, doctor_id=doctor.id,
        timeslot_id=completed_appointment.timeslot_id,
        date=completed_appointment.date, status="COMPLETED", payment_status="PAID",
    )
    db.session.add_all([appt2, appt3])
    db.session.flush()
    reviews = [
        Review(doctor_id=doctor.id, patient_id=patients[0].id,
               appointment_id=completed_appointment.id, rating=5, comment="Excellent",
               created_date=datetime.now() - timedelta(days=1)),
        Review(doctor_id=doctor.id, patient_id=patients[1].id,
               appointment_id=appt2.id, rating=4, comment="Very good",
               created_date=datetime.now() - timedelta(hours=10)),
        Review(doctor_id=doctor.id, patient_id=patients[2].id,
               appointment_id=appt3.id, rating=3, comment="Normal",
               created_date=datetime.now()),
    ]
    db.session.add_all(reviews)
    db.session.commit()
    return doctor


#  AUTH TOKENS 
@pytest.fixture
def patient_token(app, client, users):
    res = client.post("/api/auth/login", json={
        "username": users["patient_usernames"][0], 
        "password": "123"
    })
    return res.get_json()["access_token"]


@pytest.fixture
def doctor_token(app, client, users):
    res = client.post("/api/auth/login", json={
        "username": users["doctor_usernames"][0], 
        "password": "123"
    })
    return res.get_json()["access_token"]