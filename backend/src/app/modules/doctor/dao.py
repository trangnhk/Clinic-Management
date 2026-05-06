from datetime import datetime, date
from app.models import *
from app.db.db import db
from sqlalchemy import func, extract
import re

# STATIC
def get_doctor_by_user_id(user_id):
    return Doctor.query.filter_by(user_id=user_id).first()

def get_appointment_by_id(id):
    appointment = Appointment.query.get(id)

    if not appointment:
        raise ValueError("Appointment not found")
    return appointment

def get_avg_rating_by_doctor_id(doctor_id):
    raw_avg = db.session.query(func.avg(Review.rating)).filter_by(doctor_id=doctor_id).scalar()
    avg_rating = round(float(raw_avg), 1) if raw_avg else 0.0

    return avg_rating

def get_all_medicines():
    medicines = Medicine.query.order_by(Medicine.name.asc()).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "price": m.price,
            "unit": getattr(m, "unit", "viên")
        }
        for m in medicines
    ]

def get_all_tests():
    tests = Test.query.order_by(Test.name.asc()).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "price": t.price
        }
        for t in tests
    ]

# DOCTOR PROFILE
def get_doctor_profile(user_id):
    user = User.query.get(user_id)

    doctor = get_doctor_by_user_id(user_id=user_id)
    
    specialization = Specialization.query.get(doctor.specialization_id) if doctor.specialization_id else None
    return {
        "doctor_id": f"DR{str(doctor.id).zfill(9)}",
        "fullname": user.fullname,
        "phone_number": user.phone_number,
        "date_of_birth": str(user.date_of_birth) if hasattr(user, 'date_of_birth') and user.date_of_birth else None,
        "address": user.address if hasattr(user, 'address') else None,
        "specialization": specialization.name if specialization else None,
        "specialization_id": doctor.specialization_id,
        "experience_years": doctor.experience_years,
        "description": doctor.description,
        "rating": get_avg_rating_by_doctor_id(doctor.id),
        "avatar": user.avatar
    }

def update_doctor_profile(user_id, specialization_id=None, experience_years=None, description=None, fullname=None, phone_number=None):
    user = User.query.get(user_id)
    
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    if fullname is not None:
        user.fullname = fullname
    
    if phone_number is not None:
        if not re.fullmatch(r"0\d{9}", phone_number):
            raise ValueError("Invalid phone number")
        user.phone_number = phone_number

    if experience_years is not None:
        if experience_years < 0:
            raise ValueError("Invalid experience years")
        doctor.experience_years = int(experience_years)
    
    if description is not None:
        doctor.description = description
    
    db.session.commit()
    return get_doctor_profile(user_id=user_id)

def get_doctor_calendar(user_id, month: int, year: int):
    if not (1 <= month <= 12):
        raise ValueError("Invalid month")
    
    if year < 2026 or year > 2100:
        raise ValueError("Invalid year")
    
    doctor = get_doctor_by_user_id(user_id=user_id)

    schedules = DoctorSchedule.query.filter(
        DoctorSchedule.doctor_id == doctor.id,
        extract("month", DoctorSchedule.date) == month,
        extract("year", DoctorSchedule.date) == year
    ).all()

    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        extract('month', Appointment.date) == month,
        extract('year', Appointment.date) == year 
    ).all()

    calendar_data = {}

    for s in schedules:
        day = s.date.day

        if day not in calendar_data:
            calendar_data[day] = {
                "has_schedule": True,
                "appointments": []
            }


    for a in appointments:
        day = a.date.day

        if day not in calendar_data:
            # Nếu có appointment nhưng chưa có schedule
            calendar_data[day] = {
                "has_schedule": False,
                "appointments": []
            }

        calendar_data[day]["appointments"].append({
            "appointment_id": a.id,
            "status": a.status.value if hasattr(a.status, "value") else str(a.status),
            "start_time": str(a.timeslot.start_time) if a.timeslot else None
        })

    return {
        "month": month,
        "year": year,

        # Frontend sẽ highlight các ngày có lịch làm việc
        "days_with_schedule": sorted([
            day for day,data in calendar_data.items()
            if data["has_schedule"]
        ]),

        # Nếu muốn backward compatible
        "days_with_appointments": sorted([
            day for day, data in calendar_data.items()
            if len(data["appointments"]) > 0
        ]),

        "calendar": calendar_data
    }

# APPOINTMENT SCHEDULE (APPOINTMENT LIST)
def get_doctor_appointments_by_date(doctor_id, query_date):
    appointments = (
        Appointment.query
        .filter_by(doctor_id=doctor_id, date=query_date)
        .join(Appointment.timeslot)
        .order_by(TimeSlot.start_time.asc())
        .all()
    )
    return appointments

def format_appointment(a):
    status_val = a.status.value if hasattr(a.status, 'value') else str(a.status)

    return {
        "appointment_id": a.id,
        "date": str(a.date),
        "status": status_val,
        "symptoms": a.notes,
        "start_time": str(a.timeslot.start_time),
        "end_time": str(a.timeslot.end_time),
        "can_examine": status_val in [
            "WAITING_EXAMINATION",
            "PENDING_RESULT",
            "IN_PROGRESS"
        ],
        "can_complete": status_val in [
            "WAITING_EXAMINATION",
            "PENDING_RESULT",
            "COMPLETED",
            "IN_PROGRESS"
        ],
        "patient": {
            "id": a.patient.id if a.patient else None,
            "name": a.patient.user.fullname if a.patient and a.patient.user else None,
            "date_of_birth": str(a.patient.date_of_birth) if a.patient and a.patient.date_of_birth else None
        }
    }

# APPOINTMENT DETAIL (EXAMINATE)
def get_appointment_detail(appointment_id, user_id):
    doctor = get_doctor_by_user_id(user_id)
    
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")
    
    if appointment.doctor_id != doctor.id:
        raise ValueError("Forbidden: not your patient")
    
    # Examination
    exam_data = None
    if appointment.examination:
        exam = appointment.examination
        # Prescription
        prescription_data = None
        if exam.prescription:
            pres = exam.prescription
            details = []
            total_medicine = 0
            for d in pres.details:
                price = d.medicine.price if d.medicine else 0
                subtotal = price * d.quantity
                total_medicine += subtotal
                details.append({
                    "id": d.id,
                    "medicine_id": d.medicine_id,
                    "medicine_name": d.medicine.name if d.medicine else None,
                    "unit": "viên",
                    "quantity": d.quantity,
                    "unit_price": price,
                    "subtotal": subtotal,
                    "dosage": d.dosage,
                    "instruction": d.instruction
                })
            
            CONSULTATION_FEE = 500000
            prescription_data = {
                "id": pres.id,
                "details": details,
                "total_medicine_cost": total_medicine,
                "consultation_fee": CONSULTATION_FEE,
                "total": total_medicine + CONSULTATION_FEE
            }
        
        # Lab test requests
        lab_tests = []
        for tr in appointment.test_requests:
            lab_tests.append({
                "id": tr.id,
                "test_id": tr.test_id,
                "test_name": tr.test.name if tr.test else None,
                "test_price": tr.test.price if tr.test else None,
                "status": tr.status.value if hasattr(tr.status,'value') else tr.status
            })
        
        exam_data = {
            "id": exam.id,
            "created_date": str(exam.created_date),
            "diagnosis": exam.diagnosis,
            "prescription": prescription_data,
            "lab_tests": lab_tests
        }
    
    status_val = appointment.status.value if hasattr(appointment.status,'value') else appointment.status
    return {
        "appointment_id": appointment.id,
        "date": str(appointment.date),
        "status": status_val,
        "symptoms": appointment.notes if hasattr(appointment, 'notes') else None,
        "patient": {
            "id": appointment.patient.id,
            "patient_code": f"BN{str(appointment.patient.id).zfill(9)}",
            "fullname": appointment.patient.user.fullname,
            "phone_number": appointment.patient.user.phone_number,
            "email": appointment.patient.user.email,
            "date_of_birth": str(appointment.patient.date_of_birth),
            "address": appointment.patient.address
        },
        "examination": exam_data
    }

# EXAMINATION
def create_examination(appointment_id, diagnosis, user_id, symptoms=None):
    appointment = get_appointment_by_id(id=appointment_id)
    doctor = get_doctor_by_user_id(user_id=user_id)

    if not appointment:
        raise ValueError("Appointment not found")

    if doctor.id != appointment.doctor_id:
        raise ValueError("Doctor mismatch: Not your appointment")
    
    if appointment.status != AppointmentStatusEnum.WAITING_EXAMINATION:
        raise ValueError("Appointment is not in examinating")
    
    if appointment.examination:
        raise ValueError("Examination already exists for this appointment")

    if symptoms and hasattr(appointment, 'notes'):
        appointment.notes = symptoms

    exam = Examination(
        appointment_id=appointment_id,
        diagnosis=diagnosis
    )
    db.session.add(exam)

    appointment.status = AppointmentStatusEnum.IN_PROGRESS
    
    db.session.commit()
    return exam

def update_examination(exam_id, diagnosis, user_id, symptoms=None):
    exam = Examination.query.get(exam_id)
    
    if not exam:
        raise ValueError("Examination not found")
    
    appointment = get_appointment_by_id(id=exam.appointment_id)

    doctor = get_doctor_by_user_id(user_id=user_id)

    if doctor.id != appointment.doctor_id:
        raise ValueError("Doctor mismatch")
    
    if appointment.status not in [AppointmentStatusEnum.IN_PROGRESS, AppointmentStatusEnum.PENDING_RESULT]:
        raise ValueError(f"Cannot update appointment with status {appointment.status}")
    
    if diagnosis is not None:
        exam.diagnosis = diagnosis

    if symptoms is not None and hasattr(appointment, 'notes'):
        appointment.notes = symptoms
    
    db.session.commit()
    return exam

def create_or_get_prescription(exam_id, user_id):
    exam = Examination.query.get(exam_id)

    if not exam:
        raise ValueError("Examination not found")
    
    doctor = get_doctor_by_user_id(user_id)
    appointment = get_appointment_by_id(exam.appointment_id)

    if appointment.doctor_id != doctor.id:
        raise ValueError("Doctor mismatch")
    
    if exam.prescription:
        return exam.prescription
    
    pres = Prescription(examination_id=exam_id)

    db.session.add(pres)
    db.session.commit()

    return pres

def add_prescription_detail(pres_id, medicine_id, quantity, dosage, instruction, user_id):
    pres = Prescription.query.get(pres_id)
    if not pres:
        raise ValueError("Prescription not found")
    
    exam = Examination.query.get(pres.examination_id)

    doctor = get_doctor_by_user_id(user_id)
    appointment = get_appointment_by_id(id=exam.appointment_id)

    if appointment.doctor_id != doctor.id:
        raise ValueError("Forbidden")
    
    if appointment.status not in [AppointmentStatusEnum.IN_PROGRESS, AppointmentStatusEnum.PENDING_RESULT]:
        raise ValueError(f"Cannot update appointment with status {appointment.status}")

    
    medicine = Medicine.query.get(medicine_id)

    if not medicine:
        raise ValueError(f"Medicine id = {medicine_id} not found")
    
    if  quantity <= 0:
        raise ValueError("Quantity must be positive integer")
    
    detail = PrescriptionDetail(
        prescription_id=pres_id,
        medicine_id=medicine_id,
        quantity=quantity,
        dosage=dosage,
        instruction=instruction
    )

    db.session.add(detail)
    db.session.commit()

    return detail

def delete_prescription_detail(detail_id, user_id):
    
    detail = PrescriptionDetail.query.get(detail_id)
    if not detail:
        raise ValueError("Prescription detail not found")
    
    # Verify ownership
    pres = Prescription.query.get(detail.prescription_id)
    exam = Examination.query.get(pres.examination_id)
    doctor = get_doctor_by_user_id(user_id)
    appointment = get_appointment_by_id(exam.appointment_id)
    
    if appointment.doctor_id != doctor.id:
        raise ValueError("Forbidden")
    if appointment.status == AppointmentStatusEnum.COMPLETED:
        raise ValueError("Cannot modify a completed examination")
    
    db.session.delete(detail)
    db.session.commit()
    return True

def create_lab_test_request(exam_id, test_id, user_id):
    exam = Examination.query.get(exam_id)
    
    if not exam:
        raise ValueError("Examination not found")
    
    doctor = get_doctor_by_user_id(user_id)
    appointment = get_appointment_by_id(exam.appointment_id)

    if appointment.doctor_id != doctor.id:
        raise ValueError("Doctor mismatch")
    
    if appointment.status not in [AppointmentStatusEnum.IN_PROGRESS, AppointmentStatusEnum.PENDING_RESULT]:
        raise ValueError(f"Cannot add lab test: appointment is in status {appointment.status}")
    
    test = Test.query.get(test_id)
    if not test:
        raise ValueError(f"Test id={test_id} not found")
    
    existing = TestRequest.query.filter_by(
        appointment_id=appointment.id,
        test_id=test_id
    ).first()

    if existing:
        raise ValueError("Test request already exists for this appointment")
    
    test_request = TestRequest(
        appointment_id=appointment.id,
        test_id=test_id,
        status=TestStatusEnum.PENDING
    )
    db.session.add(test_request)
    
    appointment.status = AppointmentStatusEnum.PENDING_RESULT
    db.session.commit()
    return test_request

def get_lab_tests_by_exam(exam_id, user_id):
    exam = Examination.query.get(exam_id)
    if not exam:
        raise ValueError("Examination not found")
    
    doctor = get_doctor_by_user_id(user_id)
    appointment = get_appointment_by_id(exam.appointment_id)

    if appointment.doctor_id != doctor.id:
        raise ValueError("Doctor mismatch")
    
    requests = TestRequest.query.filter_by(appointment_id=appointment.id).all()

    return [{
        "id": r.id,
        "test_id": r.test_id,
        "test_name": r.test.name if r.test else None,
        "test_price": r.test.price if r.test else None,
        "status": r.status.value if hasattr(r.status, 'value') else r.status
    } for r in requests]

def delete_lab_test_request(test_request_id, user_id):
    tr = TestRequest.query.get(test_request_id)

    if not tr:
        raise ValueError("Test request not found")
    
    doctor = get_doctor_by_user_id(user_id)
    appointment = get_appointment_by_id(tr.appointment_id)

    if appointment.doctor_id != doctor.id:
        raise ValueError("Doctor mismatch")
    
    if tr.status != TestStatusEnum.PENDING:
        raise ValueError("Cannot delete: test is already in progress or done")
    
    appointment.status = AppointmentStatusEnum.IN_PROGRESS
    
    db.session.delete(tr)
    db.session.commit()
    return True

def complete_appointment(appointment_id, user_id):
    doctor = get_doctor_by_user_id(user_id)
    appointment = get_appointment_by_id(appointment_id)
    
    if appointment.doctor_id != doctor.id:
        raise ValueError("Forbidden")
    
    # Chỉ complete được nếu đã có examination
    if not appointment.examination:
        raise ValueError("Cannot complete: examination not created yet")
    
    # Không complete nếu còn lab test chưa xong
    pending_tests = [
        tr for tr in appointment.test_requests
        if (tr.status.value if hasattr(tr.status,'value') else tr.status) not in ["DONE"]
    ]
    if pending_tests:
        raise ValueError(f"Cannot complete: {len(pending_tests)} lab test(s) still pending")
    
    if appointment.status == AppointmentStatusEnum.COMPLETED:
        raise ValueError("Appointment is already completed")
    
    appointment.status = AppointmentStatusEnum.COMPLETED
    db.session.commit()
    return appointment












