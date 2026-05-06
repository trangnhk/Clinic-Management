from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

# AUTHENTICATION
@web_bp.route("/login/", methods=["GET"])
def login_page():
    return render_template("auth/login.html")

@web_bp.route("/register/", methods=["GET"])
def register_page():
    return render_template("auth/register.html")

# STATIC PAGES
@web_bp.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")

# PATIENT ROLE
@web_bp.route("/doctors/", methods=["GET"])
def doctors_page():
    return render_template("patient/doctors.html")

@web_bp.route("/book-appointment/", methods=["GET"])
def book_appointment_page():
    return render_template("patient/book_appointment.html")

@web_bp.route("/profile/", methods=["GET"])
def profile_page():
    return render_template("patient/profile.html")

@web_bp.route("/medical-history/<int:appointment_id>/", methods=["GET"])
def medical_history_page(appointment_id):
    return render_template("patient/medical_history.html", appointment_id=appointment_id)


# DOCTOR ROLE
@web_bp.route("/doctor/dashboard/", methods=["GET"])
def doctor_dashboard_page():
    return render_template("doctor/dashboard.html")

@web_bp.route("/doctor/profile/", methods=["GET"])
def doctor_profile_page():
    return render_template("doctor/profile.html")

@web_bp.route("/doctor/appointments/", methods=["GET"])
def doctor_appointments_page():
    return render_template("doctor/appointment_schedule.html")

@web_bp.route("/doctor/examination/<int:appointment_id>/", methods=["GET"])
def doctor_examination_page(appointment_id):
    return render_template("doctor/examination.html", appointment_id=appointment_id)
