from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.db.db import db
from app.models import User, Doctor, Patient

def setup_admin(app):
    admin = Admin(app, name="Clinic Admin")

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Doctor, db.session))
    admin.add_view(ModelView(Patient, db.session))

    return admin