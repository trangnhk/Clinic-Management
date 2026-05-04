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
    password_hash = Column(String(255), nullable=False)
    fullname = Column(String(100), nullable=True)
    phone_number = Column(String(10), unique=True, nullable=True)
    role = Column(Enum(RoleEnum), nullable=False, default="PATIENT")
    gender = Column(Enum(GenderEnum), nullable=True)
    is_active = Column(Boolean, default=True)
    avatar = Column(String(150), nullable=True, default="https://res.cloudinary.com/dxfbpkmen/image/upload/v1764768698/profile_efyd9k.png")

    # Relationships
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)

    def __str__(self):
        return self.fullname or self.username or f"User {self.id}"
    
    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname,
            "role": self.role,
            "gender": self.gender,
            "is_active": self.is_active,
        }

        if self.role == "PATIENT" and self.patient:
            data["patient"] = self.patient.to_dict()

        elif self.role == "DOCTOR" and self.doctor:
            data["doctor"] = self.doctor.to_dict()

        return data

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    specialization_id = Column(Integer, ForeignKey("specializations.id"))

    experience_years = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True, default=5)

    user = relationship("User", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    
    def to_dict(self):
        return {
            "id": self.id,
            "specialization_id": self.specialization_id,
            "experience_years": self.experience_years,
            "description": self.description
        }

class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)

    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")

    def to_dict(self):
        return {
            "id": self.id,
            "date_of_birth": str(self.date_of_birth) if self.date_of_birth else None,
            "address": self.address
        }


