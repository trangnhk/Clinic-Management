from app.db.db import db
from .status import SlotStatusEnum
from sqlalchemy import Column, Integer, Time, Date, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship

class TimeSlot(db.Model):
    __tablename__ = "timeslots"

    id = Column(Integer, primary_key=True)
    start_time = Column(Time)
    end_time = Column(Time)
    
    appointments = relationship("Appointment", back_populates="timeslot")

class DoctorSchedule(db.Model):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(Date)
    timeslot_id = Column(Integer, ForeignKey("timeslots.id"))
    status = Column(Enum(SlotStatusEnum), default="AVAILABLE")

    doctor = relationship("Doctor", backref="schedules", lazy=True)
    timeslot = relationship("TimeSlot", backref="schedules", lazy=True)

    __table_args__ = (
        UniqueConstraint('doctor_id', 'date', 'timeslot_id', name='unique_schedule'),
    )
    
    def to_dict(self):
        return {
            "schedule_id": self.id,
            "start_time": self.timeslot.start_time.strftime("%H:%M"),
            "end_time": self.timeslot.end_time.strftime("%H:%M"),
            "status": self.status.value
        }