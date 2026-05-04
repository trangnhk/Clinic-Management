from app.db.db import db
from .status import TestStatusEnum
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

class Test(db.Model):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    description = Column(Text)


class TestRequest(db.Model):
    __tablename__ = "test_requests"

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    status = Column(Enum(TestStatusEnum), nullable=False, default="PENDING")
    
    test_id = Column(Integer, ForeignKey("tests.id"))

    appointment = relationship("Appointment", backref="test_requests", lazy=True)
    test = relationship("Test", backref="test_requests", lazy=True)