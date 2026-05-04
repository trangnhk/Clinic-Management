from app.db.db import db
from .status import AppointmentStatusEnum, PaymentStatusEnum, TestStatusEnum
from sqlalchemy import Column, Integer, Text, Date, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    timeslot_id = Column(Integer, ForeignKey("timeslots.id"), nullable=False)
    
    date = Column(Date, nullable=False)
    status = Column(Enum(AppointmentStatusEnum), nullable=False, default=AppointmentStatusEnum.PENDING_PAYMENT)
    payment_status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
    test_status = Column(Enum(TestStatusEnum), nullable=False, default=TestStatusEnum.PENDING)

    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    timeslot = relationship("TimeSlot", back_populates="appointments")
    examination = relationship("Examination",back_populates="appointment",uselist=False)

    def __str__(self):
        return f"Appointment {self.id} - Doctor {self.doctor_id} - Patient {self.patient_id}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "timeslot_id": self.timeslot_id,
            "date": str(self.date),
            "status": self.status.value,
            "payment_status": self.payment_status,
            "test_status": self.test_status,
            "notes": self.notes
        }