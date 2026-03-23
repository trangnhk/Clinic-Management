from app.db.db import db
from .status import SlotStatusEnum
from sqlalchemy import Column, Integer, Time, Date, ForeignKey
from sqlalchemy.orm import relationship

class TimeSlot(db.Model):
    __tablename__ = "timeslots"

    id = Column(Integer, primary_key=True)
    start_time = Column(Time)
    end_time = Column(Time)


class DoctorSchedule(db.Model):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(Date)
    timeslot_id = Column(Integer, ForeignKey("timeslots.id"))
    status = Column(SlotStatusEnum, default="AVAILABLE")

    doctor = relationship("Doctor", backref="schedules", lazy=True)