import hashlib

from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, Date, ForeignKey
from app.db.db import db
from .status import RoleEnum, GenderEnum
from datetime import datetime, date
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    fullname = Column(String(100), nullable=True)
    role = Column(RoleEnum, nullable=False, default="PATIENT")
    gender = Column(GenderEnum, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    doctor = relationship("Doctor", backref="user", uselist=False, lazy=True)
    patient = relationship("Patient", backref="user", uselist=False, lazy=True)

    def __str__(self):
        return self.fullname

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    specialization_id = Column(Integer, ForeignKey("specializations.id"))

    experience_years = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    appointments = relationship("Appointment", backref="doctor", lazy=True)


class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)

    appointments = relationship("Appointment", backref="patient", lazy=True)



