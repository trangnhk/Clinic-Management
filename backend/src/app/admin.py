from flask import session, url_for, redirect, abort
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from app.db.db import db
from app.models import User, Doctor, Patient, Specialization, Appointment, Medicine, TimeSlot, DoctorSchedule, Prescription, PrescriptionDetail, Review, Test, TestRequest, Examination
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from wtforms_sqlalchemy.fields import QuerySelectField

def is_admin():
    return session.get("user_role") == "ADMIN"

class SecureAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not is_admin():
            return abort(403)
        return super().index()

    def is_accessible(self):
        return is_admin()
    
    def inaccessible_callback(self, name, **kwargs):
        return abort(403)
    
class SecureModelView(ModelView):
    def is_accessible(self):
        return is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)

class UserAdmin(SecureModelView):
    column_list = ("id", "username", "email", "role", "is_active")
    form_columns = ("username", "email", "password_hash", "role", "gender")
    form_excluded_columns = ("doctor", "patient")

    def on_model_change(self, form, model, is_created):
        if is_created or form.password_hash.data != model.password_hash:
            model.password_hash = generate_password_hash(form.password_hash.data)

class DoctorAdmin(SecureModelView):
    column_list = ("id", "user", "specialization", "experience_years")

    form_columns = ("user", "specialization", "experience_years", "description")

    form_args = {
        "user": {
            "query_factory": lambda: User.query.filter_by(role="DOCTOR"),
            "get_label": lambda u: f"{u.username} ({u.email})"
        }
    }

class PatientAdmin(SecureModelView):
    column_list = ("id", "user", "date_of_birth", "address")

    form_columns = ("user", "date_of_birth", "address")

    form_args = {
        "user": {
            "query_factory": lambda: User.query.filter_by(role="PATIENT"),
            "get_label": lambda u: f"{u.username} ({u.email})"
        }
    }

class MedicineAdmin(SecureModelView):
    column_list = ("id", "name", "price")

class SpecializationAdmin(SecureModelView):
    column_list = ("id", "name")

class ScheduleAdmin(SecureModelView):
    column_list = ("id", "doctor", "date", "timeslot", "status")

    form_columns = ("doctor", "date", "timeslot", "status")

    form_args = {
        "doctor": {
            "query_factory": lambda: Doctor.query.join(User).filter(User.role == "DOCTOR"),
            "get_label": lambda d: d.user.username if d.user else f"Doctor {d.id}"
        }
    }
    
class TimeSlotAdmin(SecureModelView):
    column_list = ("id", "start_time", "end_time")

class AppointmentAdmin(SecureModelView):
    column_list = ("id", "doctor", "patient", "date", "timeslot", "status", "payment_status", "test_status")

    form_columns = ("doctor", "patient","timeslot","date","status","payment_status","test_status","notes")

    form_args = {
        "doctor": {
            "query_factory": lambda: Doctor.query.join(User).filter(User.role == "DOCTOR"),
            "get_label": lambda d: d.user.username if d.user else f"Doctor {d.id}"
        },
        "patient": {
            "query_factory": lambda: Patient.query.join(User).filter(User.role == "PATIENT"),
            "get_label": lambda p: p.user.username if p.user else f"Patient {p.id}"
        },
        "timeslot": {
            "query_factory": lambda: TimeSlot.query.order_by(TimeSlot.start_time.asc()).all(),
            "get_label": lambda t: f"{t.start_time} - {t.end_time}"
        }
    }


class ExaminationAdmin(SecureModelView):
    column_list = ("id", "appointment", "diagnosis")

    form_columns = ("appointment", "diagnosis")

    form_args = {
        "appointment": {
            "query_factory": lambda: Appointment.query.order_by(Appointment.date.desc()).all(),
            "get_label": lambda a: f"Appointment {a.id} - {a.patient.user.username} with {a.doctor.user.username} on {a.date}"
        }
    }

class PrescriptionAdmin(SecureModelView):
    column_list = ("id", "examination")

    form_columns = ("examination",)

    form_args = {
        "examination": {
            "query_factory": lambda: Examination.query.order_by(Examination.id.desc()).all(),
            "get_label": lambda e: f"Examination {e.id} - Appointment {e.appointment.id} for {e.appointment.patient.user.username}"
        }
    }

class PrescriptionDetailAdmin(SecureModelView):
    column_list = ("id", "prescription", "medicine", "dosage", "quantity")

    form_columns = ("prescription", "medicine", "dosage", "quantity", "instruction")

    form_args = {
        "prescription": {
            "query_factory": lambda: Prescription.query.order_by(Prescription.id.desc()).all(),
            "get_label": lambda p: f"Prescription {p.id} - Examination {p.examination.id}"
        },
        "medicine": {
            "query_factory": lambda: Medicine.query.order_by(Medicine.name.asc()).all(),
            "get_label": lambda m: m.name
        }
    }

def setup_admin(app):
    if app.config.get("TESTING"):
        return None
    admin = Admin(app, name="Clinic Admin", index_view=SecureAdminIndexView())

    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(DoctorAdmin(Doctor, db.session))
    admin.add_view(PatientAdmin(Patient, db.session))
    admin.add_view(MedicineAdmin(Medicine, db.session))
    admin.add_view(SpecializationAdmin(Specialization, db.session))
    admin.add_view(ScheduleAdmin(DoctorSchedule, db.session))
    admin.add_view(TimeSlotAdmin(TimeSlot, db.session))
    admin.add_view(AppointmentAdmin(Appointment, db.session))
    admin.add_view(PrescriptionAdmin(Prescription, db.session))
    admin.add_view(ExaminationAdmin(Examination, db.session))
    admin.add_view(PrescriptionDetailAdmin(PrescriptionDetail, db.session))
    return admin