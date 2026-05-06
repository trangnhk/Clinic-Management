from app.models import User, Doctor, Patient, Appointment, AppointmentStatusEnum, Payment, PaymentTypeEnum, PaymentStatusEnum, Specialization, DoctorSchedule, SlotStatusEnum, Examination, Payment, Prescription, PrescriptionDetail, Review, Test, TestRequest
from app.db.db import db
from datetime import date, datetime, timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy import func
import re

# STATIC
def get_patient_by_user(user_id):
    patient = Patient.query.filter_by(user_id=user_id).first()

    if not patient:
        raise ValueError("Patient not found")
    
    return patient

# BOOKING FLOW
def get_all_specialization():
    return Specialization.query.all()

def get_doctor_by_specialization(specialization_id):
    if specialization_id is None:
        return Doctor.query.all()
    return Doctor.query.filter_by(specialization_id=specialization_id).all()

def get_availables_timeslots(doctor_id, date):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise Exception("Doctor not found")
    
    schedules = DoctorSchedule.query.filter_by(
        doctor_id=doctor_id,
        date=date,
        status="AVAILABLE"
    ).all()

    return [s.to_dict() for s in schedules]

def create_appointment(patient_id, doctor_id, schedule_id, date, notes):
    # schedule = DoctorSchedule.query.get(schedule_id)
    schedule = DoctorSchedule.query.with_for_update().get(schedule_id)
    
    if not schedule:
        raise ValueError("Schedule not found")
    
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    if date < datetime.now().date():
        raise ValueError("Cannot book past date")

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise ValueError("Doctor not found")
    
    if schedule.doctor_id != doctor_id:
        raise ValueError("Doctor mismatch")

    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    if schedule.date != date:
        raise ValueError("Date mismatch")

    if schedule.status != "AVAILABLE":
        raise ValueError("Slot already booked")
    print(type(schedule.date), schedule.date)
    print(type(date), date)

    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        timeslot_id=schedule.timeslot_id,
        date=date,
        status="PENDING_PAYMENT",
        notes=notes
    )

    # update slot
    schedule.status = "BOOKED"

    db.session.add(appointment)
    db.session.commit()

    return appointment

# PAYMENT FLOW
def make_payment(appointment_id, amount, user_id):
    MIN_DEPOSIT = 100000

    if amount < MIN_DEPOSIT:
        raise ValueError("Minimum deposit is 100,000")

    appt = Appointment.query.get(appointment_id)

    if not appt:
        raise ValueError("Appointment not found")

    patient = get_patient_by_user(user_id)

    if appt.patient_id != patient.id:
        raise ValueError("Not your appointment")

    if appt.payment_status == PaymentStatusEnum.PAID:
        raise ValueError("Already paid")

    if appt.status != AppointmentStatusEnum.PENDING_PAYMENT:
        raise ValueError("Invalid appointment status")

    payment = Payment(
        appointment_id=appointment_id,
        payment_type=PaymentTypeEnum.DEPOSIT,
        amount=amount,
        status=PaymentStatusEnum.PAID,
        paid_at=datetime.now()
    )

    db.session.add(payment)

    appt.payment_status = PaymentStatusEnum.PAID
    appt.status = AppointmentStatusEnum.WAITING_EXAMINATION
    # db.session.commit()

    schedule = DoctorSchedule.query.filter_by(
        doctor_id=appt.doctor_id,
        date=appt.date,
        timeslot_id=appt.timeslot_id
    ).first()

    if schedule:
        schedule.status = SlotStatusEnum.BLOCKED

    db.session.commit()


    return payment

def auto_cancel_unpaid():
    expired = datetime.now() - timedelta(minutes=30)

    appts = Appointment.query.filter(
        Appointment.status == AppointmentStatusEnum.PENDING_PAYMENT,
        Appointment.created_at <= expired
    ).all()

    for appt in appts:
        appt.status = AppointmentStatusEnum.CANCELED
        appt.payment_status = PaymentStatusEnum.FAILED

        schedule = DoctorSchedule.query.filter_by(
            doctor_id=appt.doctor_id,
            date=appt.date,
            timeslot_id=appt.timeslot_id
        ).first()

        if schedule:
            schedule.status = SlotStatusEnum.AVAILABLE

    db.session.commit()

# APPOINTMENT FLOW
def cancel_appointment(appointment_id, user_id):
    patient = get_patient_by_user(user_id=user_id)

    appt = Appointment.query.get(appointment_id)

    if not appt:
        raise ValueError("Appointment not found")

    if appt.patient_id != patient.id:
        raise ValueError("Forbidden")

    if appt.status in ["COMPLETED", "CANCELED"]:
        raise ValueError("Cannot cancel")

    appt.status = "CANCELED"

    schedule = DoctorSchedule.query.filter_by(
        doctor_id=appt.doctor_id,
        date=appt.date,
        timeslot_id=appt.timeslot_id
    ).first()

    if schedule:
        schedule.status = SlotStatusEnum.AVAILABLE

    db.session.commit()

    return appt

def get_patient_appointments(patient_id, status=None):
    query = Appointment.query.filter_by(patient_id=patient_id)

    if status:
        query = query.filter_by(status=status)

    return query.order_by(Appointment.date.desc()).all()

def get_appointment_detail_dao(appt: Appointment, user_id):
    patient = get_patient_by_user(user_id)

    return {
        "patient": {
            "id": patient.id,
            "fullname": patient.user.fullname if patient.user is not None else None,
            "date_of_birth": patient.date_of_birth,
            "address": patient.address,
            "phone_number": patient.user.phone_number if patient.user is not None else None,
            "email": patient.user.email if patient.user is not None else None
        },
        "appointment_id": appt.id,
        "date": str(appt.date),
        "status": appt.status,
        "doctor": appt.doctor.user.fullname,
        "start_time": str(appt.timeslot.start_time),
        "end_time": str(appt.timeslot.end_time)
    }

# PROFILE
def get_patient_profile(user_id, page, per_page):
    patient = get_patient_by_user(user_id)
    
    # appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    pagination = Appointment.query.filter_by(patient_id=patient.id)\
        .order_by(Appointment.date.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    
    if pagination.pages == 0:
        return {
            "profile": {
                "id": f"{patient.id:06d}",
                "fullname": patient.user.fullname,
                "phone_number": patient.user.phone_number,
                "email": patient.user.email,
                "date_of_birth": str(patient.date_of_birth) if patient.date_of_birth else None,
                "address": patient.address,
                "avatar": patient.user.avatar if patient.user and patient.user.avatar else None
            },
            "appointments": [],
            "pagination": {
                "page": 1,
                "per_page": per_page,
                "total": 0,
                "pages": 0
            },
            "laboratory_results": []
        }

    if page > pagination.pages:
        raise ValueError(f"Page out of range. Max page is {pagination.pages}")
    
    
    print("Requested page:", page)
    print("Actual page from pagination:", pagination.page)

    lab_rows = (
        TestRequest.query
        .join(Appointment, TestRequest.appointment_id == Appointment.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .join(User, Doctor.user_id == User.id)
        .join(Test, TestRequest.test_id == Test.id)
        .filter(Appointment.patient_id == patient.id)
        .order_by(Appointment.date.desc(), TestRequest.id.desc())
        .all()
    )

    laboratory_results = [
        {
            "appointment_id": row.appointment_id,
            "date": str(row.appointment.date) if row.appointment else None,
            "doctor_name": row.appointment.doctor.user.fullname
                if row.appointment and row.appointment.doctor and row.appointment.doctor.user
                else None,
            "test_name": row.test.name if row.test else None,
            "status": row.status.value if hasattr(row.status, "value") else str(row.status)
        }
        for row in lab_rows
    ]


    return {
        "profile": {
            "id": f"{patient.id:06d}",
            "fullname": patient.user.fullname,
            "phone_number": patient.user.phone_number,
            "email": patient.user.email,
            "date_of_birth": str(patient.date_of_birth) if patient.date_of_birth else None,
            "address": patient.address,
            "avatar": patient.user.avatar if patient.user and patient.user.avatar else None
        },
        "appointments": pagination.items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages
        },
        "laboratory_results": laboratory_results
    }

def update_patient_profile(user_id, date_of_birth=None, address=None, fullname=None, phone_number=None):
    patient = get_patient_by_user(user_id)
    # Validate date
    if date_of_birth is not None:
        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except:
            raise ValueError("Invalid date")

    # Validate phone
    if phone_number is not None:
        if not re.fullmatch(r"\d{10}", phone_number):
            raise ValueError("Invalid phone number")

    # Update the patient's information
    patient.date_of_birth = date_of_birth if date_of_birth is not None else patient.date_of_birth
    patient.address = address if address is not None else patient.address
    patient.user.fullname = fullname if fullname is not None else patient.user.fullname
    patient.user.phone_number = phone_number if phone_number is not None else patient.user.phone_number

    db.session.commit()
    return patient

# MEDICAL
def get_medical_history_detail(appointment):
    
    appointment = Appointment.query.options(
        joinedload(Appointment.doctor).joinedload(Doctor.user),
        joinedload(Appointment.patient).joinedload(Patient.user),
        joinedload(Appointment.timeslot),
        joinedload(Appointment.examination)
            .joinedload(Examination.prescription)
            .joinedload(Prescription.details)
            .joinedload(PrescriptionDetail.medicine),
            joinedload(Appointment.test_requests).joinedload(TestRequest.test)
    ).filter_by(id=appointment.id).first()

    examination = appointment.examination

    if not examination:
        raise ValueError("Examination not found")
    
    prescription = examination.prescription
    prescription_items = []
    medicine_total = 0

    if prescription:
        for idx, item in enumerate(prescription.details, start=1):

            unit_price = item.medicine.price if item.medicine else 0
            line_total = unit_price * item.quantity
            medicine_total += line_total

            prescription_items.append({
                "no": idx,
                "medicine_id": item.medicine.id if item.medicine else None,
                "medicine_name": item.medicine.name if item.medicine else None,
                "dosage": item.dosage,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "amount": line_total,
                "instruction": item.instruction
            })


    payments = Payment.query.filter_by(appointment_id=appointment.id).all()
    paid_payments = [p for p in payments if p.status == PaymentStatusEnum.PAID]
    payment_summary = {
        "deposit": 0,
        "medicine": 0,
        "lab_test": 0,
        "final": 0
    }
    payment_items = []
    total_paid = 0

    for p in paid_payments:
        amount = p.amount

        payment_type = p.payment_type.value

        if payment_type == "DEPOSIT":
            payment_summary["deposit"] += amount

        elif payment_type == "MEDICINE":
            payment_summary["medicine"] += amount

        elif payment_type == "LAB_TEST":
            payment_summary["lab_test"] += amount

        elif payment_type == "FINAL":
            payment_summary["final"] += amount

        payment_items.append({
            "payment_id": p.id,
            "type": payment_type,
            "amount": amount,
            "paid_at": p.paid_at.isoformat() if p.paid_at else None
        })
    total_paid = payment_summary["deposit"] + payment_summary["final"]
    print("Payment summary:", payment_summary)
    print("Total paid:", total_paid)

    test_results = []
    for tr in appointment.test_requests:
        test_results.append({
            "test_request_id": tr.id,
            "test_name": tr.test.name if tr.test else None,
            "status": tr.status.value if hasattr(tr.status, "value") else str(tr.status)
        })

    return {
        "appointment_info": {
            "id": appointment.id,
            "date": str(appointment.date),
            "status": appointment.status.value,
            "start_time": str(appointment.timeslot.start_time),
            "end_time": str(appointment.timeslot.end_time),
            "notes": appointment.notes
        },

        "patient_info": {
            "id": appointment.patient.id,
            "fullname": appointment.patient.user.fullname,
            "email": appointment.patient.user.email,
            "phone_number": appointment.patient.user.phone_number,
            "date_of_birth": str(appointment.patient.date_of_birth) if appointment.patient.date_of_birth else None,
            "address": appointment.patient.address
        },

        "doctor_info": {
            "id": appointment.doctor.id,
            "fullname": appointment.doctor.user.fullname
        },

        "medical_result": {
            "diagnosis": examination.diagnosis
        },

        "prescription": {
            "items": prescription_items,
            "total_medicine_cost": medicine_total
        },

        "payment": {
            "items": payment_items,
            "summary": payment_summary,
            "total_paid": total_paid
        },
        "test_results": test_results
    }

# REVIEW
def create_review(appt_id, rating, comment, user_id):
    patient = get_patient_by_user(user_id)

    appt = Appointment.query.get(appt_id)

    existed = Review.query.filter_by(appointment_id=appt_id).first()

    if existed:
        raise ValueError("Already reviewed")
    
    if rating < 1 or rating > 5:
        raise ValueError("Invalid rating")

    review = Review(
        doctor_id=appt.doctor_id,
        patient_id=patient.id,
        appointment_id=appt_id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return review

def get_doctor_reviews(doctor_id):
    reviews = Review.query.filter_by(doctor_id=doctor_id)\
        .order_by(Review.created_date.desc())\
        .all()

    avg_rating = db.session.query(func.avg(Review.rating)).filter_by(doctor_id=doctor_id).scalar()

    total_reviews = Review.query.filter_by(doctor_id=doctor_id).count()

    breakdown = {}

    for star in range(1, 6):
        count = Review.query.filter_by(
            doctor_id=doctor_id,
            rating=star
        ).count()

        breakdown[str(star)] = count

    return {
        "doctor_id": doctor_id,
        "average_rating": round(float(avg_rating), 1) if avg_rating else 0,
        "total_reviews": total_reviews,
        "rating_breakdown": breakdown,
        "reviews": reviews
    }




