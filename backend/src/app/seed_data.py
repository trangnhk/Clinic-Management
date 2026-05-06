import random
from datetime import datetime, date, timedelta
from app.db.db import db
from app.models import *
from app.modules.user.dao import hash_password
from app.models.status import (
    RoleEnum, GenderEnum, SlotStatusEnum,
    AppointmentStatusEnum, PaymentStatusEnum,
    PaymentTypeEnum, TestStatusEnum
)

FULLNAMES_PATIENT = [
    "Nguyễn Văn An", "Trần Thị Bích", "Lê Văn Cường",
    "Phạm Thị Dung", "Hoàng Văn Em"
]
FULLNAMES_DOCTOR = [
    "BS. Nguyễn Minh Khoa", "BS. Trần Thị Lan", "BS. Lê Quốc Hùng",
    "BS. Phạm Thị Mai", "BS. Đỗ Văn Nam", "BS. Vũ Thị Oanh",
    "BS. Bùi Văn Phong", "BS. Ngô Thị Quỳnh", "BS. Đinh Văn Sơn",
    "BS. Lý Thị Tuyết"
]
ADDRESSES = [
    "123 Lê Lợi, Q.1, TP.HCM",
    "456 Nguyễn Huệ, Q.1, TP.HCM",
    "789 Trần Hưng Đạo, Q.5, TP.HCM",
    "101 Điện Biên Phủ, Q.3, TP.HCM",
    "202 Cách Mạng Tháng 8, Q.10, TP.HCM",
]


# =========================
# USERS
# =========================
def seed_users():
    print("Seeding users...")

    # ===== PATIENT =====
    for i in range(5):
        username = f"patient{i}"
        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(
                username=username,
                email=f"{username}@mail.com",
                password_hash=hash_password("123"),
                fullname=FULLNAMES_PATIENT[i],
                role=RoleEnum.PATIENT,
                gender=random.choice([GenderEnum.MALE, GenderEnum.FEMALE]),
                is_active=True
            )
            db.session.add(user)
            db.session.flush()
        patient = Patient.query.filter_by(user_id=user.id).first()
        if patient:
            patient.date_of_birth = date(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28))
            patient.address = random.choice(ADDRESSES)
            # db.session.commit()

    # ===== DOCTOR =====
    specializations = Specialization.query.all()

    for i in range(10):
        username = f"doctor{i}"
        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(
                username=username,
                email=f"{username}@mail.com",
                password_hash=hash_password("123"),
                fullname=FULLNAMES_DOCTOR[i],
                role=RoleEnum.DOCTOR,
                gender=random.choice([GenderEnum.MALE, GenderEnum.FEMALE]),
                is_active=True
            )
            db.session.add(user)
            db.session.flush()

        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if doctor :
            doctor.specialization_id = random.choice(specializations).id if specializations else None
            doctor.experience_years = random.randint(2, 20)
            doctor.description = "Bác sĩ có nhiều năm kinh nghiệm trong lĩnh vực chuyên môn."
            doctor.rating = random.randint(3, 5)
            # db.session.commit()

    db.session.commit()


# =========================
# SPECIALIZATION
# =========================
def seed_specializations():
    print("Seeding specializations...")
    specs = [
        ("Cardiology", "Chuyên khoa tim mạch"),
        ("Dermatology", "Chuyên khoa da liễu"),
        ("Neurology", "Chuyên khoa thần kinh"),
        ("Pediatrics", "Chuyên khoa nhi"),
        ("ENT", "Tai mũi họng"),
        ("General", "Nội tổng quát"),
    ]

    for name, desc in specs:
        if not Specialization.query.filter_by(name=name).first():
            db.session.add(Specialization(name=name, description=desc))

    db.session.commit()


# =========================
# MEDICINE
# =========================
def seed_medicines():
    print("Seeding medicines...")
    if Medicine.query.count() >= 20:
        return

    for i in range(20):
        name = f"Medicine {i}"
        if not Medicine.query.filter_by(name=name).first():
            db.session.add(Medicine(
                name=name,
                price=round(random.uniform(10, 100), 2),
                description=f"Thuốc {name} dùng điều trị các bệnh thông thường."
            ))

    db.session.commit()


# =========================
# TIMESLOTS
# =========================
def seed_timeslots():
    print("Seeding timeslots...")
    if TimeSlot.query.first():
        return

    start = datetime.strptime("08:00", "%H:%M")
    end = datetime.strptime("20:00", "%H:%M")

    while start < end:
        slot_end = start + timedelta(minutes=30)
        db.session.add(TimeSlot(
            start_time=start.time(),
            end_time=slot_end.time()
        ))
        start = slot_end

    db.session.commit()


# =========================
# DOCTOR SCHEDULE
# =========================
def seed_doctor_schedules():
    print("Seeding doctor schedules...")
    doctors = Doctor.query.all()
    timeslots = TimeSlot.query.all()

    for doctor in doctors:
        count = 0
        while count < 10:
            date_val = date.today() + timedelta(days=random.randint(0, 5))
            slot = random.choice(timeslots)

            exists = DoctorSchedule.query.filter_by(
                doctor_id=doctor.id,
                date=date_val,
                timeslot_id=slot.id
            ).first()

            if exists:
                continue

            db.session.add(DoctorSchedule(
                doctor_id=doctor.id,
                date=date_val,
                timeslot_id=slot.id,
                status=SlotStatusEnum.AVAILABLE
            ))
            count += 1

    db.session.commit()


# =========================
# APPOINTMENT
# =========================
def seed_appointments():
    print("Seeding appointments...")
    patients = Patient.query.all()
    schedules = DoctorSchedule.query.filter_by(status=SlotStatusEnum.AVAILABLE).all()

    for schedule in schedules:
        exists = Appointment.query.filter_by(
            doctor_id=schedule.doctor_id,
            timeslot_id=schedule.timeslot_id,
            date=schedule.date
        ).first()

        if exists:
            continue

        appt_status = random.choice([
            AppointmentStatusEnum.PENDING_PAYMENT,
            AppointmentStatusEnum.WAITING_EXAMINATION,
            AppointmentStatusEnum.COMPLETED,
            AppointmentStatusEnum.CANCELED,
        ])

        # Xác định payment_status và test_status theo business logic
        if appt_status == AppointmentStatusEnum.PENDING_PAYMENT:
            payment_status = PaymentStatusEnum.PENDING
            test_status = TestStatusEnum.PENDING
            schedule.status = SlotStatusEnum.BOOKED

        elif appt_status == AppointmentStatusEnum.WAITING_EXAMINATION:
            payment_status = PaymentStatusEnum.PAID
            test_status = TestStatusEnum.PENDING
            schedule.status = SlotStatusEnum.BLOCKED

        elif appt_status == AppointmentStatusEnum.COMPLETED:
            payment_status = PaymentStatusEnum.PAID
            test_status = random.choice([TestStatusEnum.DONE, TestStatusEnum.PENDING])
            schedule.status = SlotStatusEnum.BLOCKED

        else:  # CANCELED
            payment_status = random.choice([PaymentStatusEnum.FAILED, PaymentStatusEnum.PAID])
            test_status = TestStatusEnum.PENDING
            schedule.status = SlotStatusEnum.AVAILABLE

        appt = Appointment(
            doctor_id=schedule.doctor_id,
            patient_id=random.choice(patients).id,
            timeslot_id=schedule.timeslot_id,
            date=schedule.date,
            status=appt_status,
            payment_status=payment_status,
            test_status=test_status
        )
        db.session.add(appt)

    db.session.commit()


# =========================
# PAYMENT
# =========================
def seed_payments():
    print("Seeding payments...")

    DEPOSIT = 100000
    CONSULTATION = 500000

    appointments = Appointment.query.all()

    for appt in appointments:

        if Payment.query.filter_by(appointment_id=appt.id).first():
            continue

        # =============================
        # PENDING PAYMENT
        # =============================
        if appt.status == AppointmentStatusEnum.PENDING_PAYMENT:

            db.session.add(Payment(
                appointment_id=appt.id,
                payment_type=PaymentTypeEnum.DEPOSIT,
                amount=DEPOSIT,
                status=PaymentStatusEnum.PENDING,
                paid_at=None
            ))

            # slot booked
            schedule = DoctorSchedule.query.filter_by(
                doctor_id=appt.doctor_id,
                date=appt.date,
                timeslot_id=appt.timeslot_id
            ).first()

            if schedule:
                schedule.status = SlotStatusEnum.BOOKED

        # =============================
        # WAITING EXAMINATION
        # =============================
        elif appt.status == AppointmentStatusEnum.WAITING_EXAMINATION:

            db.session.add(Payment(
                appointment_id=appt.id,
                payment_type=PaymentTypeEnum.DEPOSIT,
                amount=DEPOSIT,
                status=PaymentStatusEnum.PAID,
                paid_at=datetime.now()
            ))

            schedule = DoctorSchedule.query.filter_by(
                doctor_id=appt.doctor_id,
                date=appt.date,
                timeslot_id=appt.timeslot_id
            ).first()

            if schedule:
                schedule.status = SlotStatusEnum.BLOCKED

        # =============================
        # COMPLETED
        # =============================
        elif appt.status == AppointmentStatusEnum.COMPLETED:

            paid_time = datetime.now()

            # Deposit
            db.session.add(Payment(
                appointment_id=appt.id,
                payment_type=PaymentTypeEnum.DEPOSIT,
                amount=DEPOSIT,
                status=PaymentStatusEnum.PAID,
                paid_at=paid_time - timedelta(hours=2)
            ))

            # ======================
            # Medicine Cost
            # ======================
            medicine_cost = 0

            exam = Examination.query.filter_by(
                appointment_id=appt.id
            ).first()

            if exam and exam.prescription:
                for item in exam.prescription.details:
                    medicine_cost += item.quantity * item.medicine.price

            if medicine_cost > 0:
                db.session.add(Payment(
                    appointment_id=appt.id,
                    payment_type=PaymentTypeEnum.MEDICINE,
                    amount=medicine_cost,
                    status=PaymentStatusEnum.PAID,
                    paid_at=paid_time - timedelta(hours=1)
                ))

            # ======================
            # Lab Cost
            # ======================
            lab_cost = 0

            tests = TestRequest.query.filter_by(
                appointment_id=appt.id
            ).all()

            for t in tests:
                if t.test:
                    lab_cost += t.test.price

            if lab_cost > 0:
                db.session.add(Payment(
                    appointment_id=appt.id,
                    payment_type=PaymentTypeEnum.LAB_TEST,
                    amount=lab_cost,
                    status=PaymentStatusEnum.PAID,
                    paid_at=paid_time - timedelta(minutes=30)
                ))

            # ======================
            # Final Payment
            # ======================
            final_amount = (
                CONSULTATION - DEPOSIT
                + medicine_cost
                + lab_cost
            )

            db.session.add(Payment(
                appointment_id=appt.id,
                payment_type=PaymentTypeEnum.FINAL,
                amount=final_amount,
                status=PaymentStatusEnum.PAID,
                paid_at=paid_time
            ))

            schedule = DoctorSchedule.query.filter_by(
                doctor_id=appt.doctor_id,
                date=appt.date,
                timeslot_id=appt.timeslot_id
            ).first()

            if schedule:
                schedule.status = SlotStatusEnum.BLOCKED

        # =============================
        # CANCELED
        # =============================
        elif appt.status == AppointmentStatusEnum.CANCELED:

            db.session.add(Payment(
                appointment_id=appt.id,
                payment_type=PaymentTypeEnum.DEPOSIT,
                amount=DEPOSIT,
                status=PaymentStatusEnum.FAILED,
                paid_at=None
            ))

            schedule = DoctorSchedule.query.filter_by(
                doctor_id=appt.doctor_id,
                date=appt.date,
                timeslot_id=appt.timeslot_id
            ).first()

            if schedule:
                schedule.status = SlotStatusEnum.AVAILABLE

    db.session.commit()

# =========================
# EXAMINATION
# =========================
def seed_examinations():
    print("Seeding examinations...")
    # Tạo examination cho cả WAITING_EXAMINATION và COMPLETED
    target_statuses = [
        AppointmentStatusEnum.WAITING_EXAMINATION,
        AppointmentStatusEnum.COMPLETED
    ]
    appointments = Appointment.query.filter(
        Appointment.status.in_(target_statuses)
    ).all()

    diagnoses = ["Flu", "Hypertension", "Diabetes Type 2", "Allergic Rhinitis", "Gastritis"]

    for appt in appointments:
        if Examination.query.filter_by(appointment_id=appt.id).first():
            continue

        db.session.add(Examination(
            appointment_id=appt.id,
            diagnosis=random.choice(diagnoses)
        ))

    db.session.commit()


# =========================
# PRESCRIPTION
# =========================
def seed_prescriptions():
    print("Seeding prescriptions...")
    exams = Examination.query.all()
    medicines = Medicine.query.all()

    for exam in exams:
        if Prescription.query.filter_by(examination_id=exam.id).first():
            continue

        if random.choice([True, False]):
            pres = Prescription(examination_id=exam.id)
            db.session.add(pres)
            db.session.flush()

            used = set()
            num_medicines = random.randint(1, 3)
            while len(used) < num_medicines:
                med = random.choice(medicines)
                if med.id in used:
                    continue
                used.add(med.id)

                db.session.add(PrescriptionDetail(
                    prescription_id=pres.id,
                    medicine_id=med.id,
                    dosage=random.choice(["1 lần/ngày", "2 lần/ngày", "3 lần/ngày"]),
                    quantity=random.randint(5, 30),
                    instruction=random.choice(["Uống sau ăn", "Uống trước ăn", "Uống khi cần"])
                ))

    db.session.commit()


# =========================
# TEST
# =========================
def seed_tests():
    print("Seeding tests...")
    test_data = [
        ("Xét nghiệm máu", 50, "Kiểm tra công thức máu toàn phần"),
        ("Chụp X-quang", 100, "Chụp X-quang ngực thẳng"),
        ("Siêu âm bụng", 150, "Siêu âm ổ bụng tổng quát"),
        ("Điện tâm đồ", 80, "Đo điện tim"),
        ("Xét nghiệm nước tiểu", 30, "Phân tích nước tiểu toàn phần"),
    ]

    for name, price, desc in test_data:
        if not Test.query.filter_by(name=name).first():
            db.session.add(Test(name=name, price=price, description=desc))
    db.session.commit()

    tests = Test.query.all()
    appointments = Appointment.query.filter(
        Appointment.status.in_([
            AppointmentStatusEnum.WAITING_EXAMINATION,
            AppointmentStatusEnum.COMPLETED
        ])
    ).all()

    for appt in appointments:
        if TestRequest.query.filter_by(appointment_id=appt.id).first():
            continue

        if random.choice([True, False]):
            status = (
                TestStatusEnum.DONE
                if appt.status == AppointmentStatusEnum.COMPLETED
                else random.choice([TestStatusEnum.PENDING, TestStatusEnum.IN_PROGRESS])
            )
            db.session.add(TestRequest(
                appointment_id=appt.id,
                test_id=random.choice(tests).id,
                status=status
            ))

    db.session.commit()


# =========================
# REVIEW
# =========================
def seed_reviews():
    print("Seeding reviews...")
    completed = Appointment.query.filter_by(status=AppointmentStatusEnum.COMPLETED).all()

    comments = [
        "Bác sĩ rất tận tâm và chuyên nghiệp.",
        "Khám bệnh nhanh, chẩn đoán chính xác.",
        "Bác sĩ giải thích rõ ràng, dễ hiểu.",
        "Rất hài lòng với dịch vụ khám bệnh.",
        "Bác sĩ thân thiện và nhiệt tình."
    ]

    for appt in completed:
        if Review.query.filter_by(appointment_id=appt.id).first():
            continue

        if random.choice([True, False]):
            db.session.add(Review(
                doctor_id=appt.doctor_id,
                patient_id=appt.patient_id,
                appointment_id=appt.id,
                rating=random.randint(3, 5),
                comment=random.choice(comments)
            ))

    db.session.commit()


# =========================
# MAIN SEED
# =========================
def run_seed():
    print("Seeding database...")

    seed_specializations()
    seed_users()
    seed_medicines()
    seed_timeslots()
    seed_doctor_schedules()

    seed_appointments()
    seed_examinations()
    seed_prescriptions()
    seed_tests()

    seed_payments()   # PHẢI ĐỂ SAU CÙNG

    seed_reviews()

    print("Seeding completed!")
