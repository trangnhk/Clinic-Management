from app.db.db import db
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Examination(db.Model):
    __tablename__ = "examinations"

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    diagnosis = Column(Text, nullable=True)

    prescription = relationship("Prescription", backref="examination", uselist=False, lazy=True)