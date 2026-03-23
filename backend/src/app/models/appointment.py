from app.db.db import db
from .status import AppointmentStatusEnum, PaymentStatusEnum, TestStatusEnum
from sqlalchemy import Column, Integer, Text, Date, ForeignKey


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    Date = Column(Date, nullable=False)

    status = Column(AppointmentStatusEnum, nullable=False, default="WAITING_EXAMINATION")
    payment_status = Column(PaymentStatusEnum, nullable=False, default="PENDING")
    test_status = Column(TestStatusEnum, nullable=False, default="PEDING")

    notes = Column(Text, nullable=True)

    def __str__(self):
        return f"Appointment {self.id} - Doctor {self.doctor_id} - Patient {self.patient_id}"