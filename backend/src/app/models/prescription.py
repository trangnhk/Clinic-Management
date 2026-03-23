from app.db.db import db
from sqlalchemy import Column, Integer, Text, Enum, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship

class Prescription(db.Model):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True)
    examination_id = Column(Integer, ForeignKey("examinations.id"))

    details = relationship("PrescriptionDetail", backref="prescription", lazy=True)


class Medicine(db.Model):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    description = Column(Text)


class PrescriptionDetail(db.Model):
    __tablename__ = "prescription_details"

    id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))

    dosage = Column(String(100))
    quantity = Column(Integer)
    instruction = Column(Text)

    medicine = relationship("Medicine", backref="prescription_details", lazy=True)