from app.db.db import db
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Review(db.Model):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    rating = Column(Integer, nullable=False, default=5)
    comment = Column(String(500), nullable=True)
    created_date = Column(DateTime, default=func.now())

    doctor = relationship("Doctor", backref="reviews", lazy=True)
    patient = relationship("Patient", backref="reviews", lazy=True)

    appointment = relationship("Appointment", backref="review", uselist=False, lazy=True)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    def __str__(self):
        return f"Review(comment={self.comment}, doctor_id={self.doctor_id}, patient_id={self.patient_id}, rating={self.rating}, comment='{self.comment}', created_date={self.created_date})"