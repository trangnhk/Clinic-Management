from flask import session, url_for, redirect, abort, render_template_string, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from app.db.db import db
from app.models import User, Doctor, Patient, Specialization, Appointment, Medicine, TimeSlot, DoctorSchedule, Prescription, PrescriptionDetail, Review, Test, TestRequest, Examination
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from werkzeug.security import generate_password_hash
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, NumberRange, Regexp
from datetime import time
from wtforms import DecimalField


def is_admin():
    return session.get("user_role") == "ADMIN"

class SecureAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not is_admin():
            return abort(403)
        return super().index()
    
    @expose("/logout")
    def logout_view(self):
        session.clear()

        return render_template_string("""
            <script>

                localStorage.removeItem("access_token");
                localStorage.removeItem("user");

                window.location.href = "/login";

            </script>
        """)

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
    column_list = ("id", "username", "email", "role", "is_active", "phone_number")
    form_columns = ("username", "email", "password_hash", "role", "gender", "phone_number")
    form_excluded_columns = ("doctor", "patient")

    form_args = {
        "password_hash": {
            "validators": [
                DataRequired(message="Password is required")
            ]
        },
        "email": {
            "validators": [
                DataRequired(message="Email is required"),
                Regexp(r'^[^@]+@[^@]+\.[^@]+$', message="Invalid email format")
            ]
        }
    }

    def on_model_change(self, form, model, is_created):
        existing_username = User.query.filter(db.func.lower(User.username) == model.username.lower()).first()

        if is_created:
            if existing_username:
                raise ValidationError("Username already exists")

        else:
            if (existing_username and existing_username.id != model.id):
                raise ValidationError("Username already exists")
        
        existing_email = User.query.filter(db.func.lower(User.email) == model.email.lower()).first()

        if is_created:
            if existing_email:
                raise ValidationError("Email already exists")
        else:
            if (existing_email and existing_email.id != model.id):
                raise ValidationError("Email already exists")

        # hash password
        if (is_created or form.password_hash.data != model.password_hash):
            model.password_hash = generate_password_hash(form.password_hash.data)


class DoctorAdmin(SecureModelView):
    column_list = ("id", "user", "specialization", "experience_years")

    form_columns = ("user", "specialization", "experience_years", "description")

    form_args = {
        "user": {
            "query_factory": lambda: User.query.filter_by(role="DOCTOR"),
            "get_label": lambda u: f"{u.username} ({u.email})"
        },
        "experience_years":{
            "validators": [
                NumberRange(min=0, message="Experience years must be a non-negative integer")
            ]
        }
    }

    def delete_model(self, model):
        try:
            # Check doctor schedules
            has_schedule = DoctorSchedule.query.filter_by(doctor_id=model.id).first()

            if has_schedule:
                raise Exception("Cannot delete doctor because doctor has schedules")

            db.session.delete(model)
            db.session.commit()

            return True

        except Exception as ex:
            db.session.rollback()

            flash(str(ex), "error")

            return False


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
    form_columns = ("name", "price", "description")
    form_overrides = {
        "price": DecimalField
    }

    form_args = {
        "name": {
            "validators": [
                DataRequired(message="Medicine name is required")
            ]
        },

        "price": {
            "validators": [
                DataRequired(message="Price is required"),
                NumberRange(min=0.01, message="Price must be > 0")
            ]
        }
    }


class SpecializationAdmin(SecureModelView):
    column_list = ("id", "name")
    form_columns = ("name", "description")

    def on_model_change(self, form, model, is_created):
        # validate empty
        if not model.name:
            raise ValidationError("Specialization name is required")
        
        name = " ".join(model.name.strip().split())
        specializations = Specialization.query.all()

        for s in specializations:
            if s is model:
                continue

            # CREATE
            if is_created:

                if s.name and s.name.strip().lower() == name.lower():
                    raise ValidationError("Specialization name already exists")

            # UPDATE
            else:
                if (s.id != model.id and s.name and s.name.strip().lower() == name.lower()):
                    raise ValidationError("Specialization name already exists")

        model.name = name

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

    def on_model_change(self, form, model, is_created):

        # Validate start_time >= 08:00
        if model.start_time < time(8, 0):
            raise ValidationError(
                "Start time must be greater than or equal to 08:00"
            )

        # Validate end_time <= 20:00
        if model.end_time > time(20, 0):
            raise ValidationError(
                "End time must be less than or equal to 20:00"
            )

        # Validate start_time < end_time
        if model.start_time >= model.end_time:
            raise ValidationError(
                "Start time must be before end time"
            )

        return super().on_model_change(form, model, is_created)

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
    admin = Admin(app, name="Clinic Admin", index_view=SecureAdminIndexView(), template_mode="bootstrap4")

    admin.add_link(MenuLink(
        name="Logout",
        category="",
        url="/admin/logout"
    ))
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