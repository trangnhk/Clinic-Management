from app.db.db import db
from .status import PaymentStatusEnum, PaymentTypeEnum
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

class Payment(db.Model):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))

    status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
    payment_type = Column(Enum(PaymentTypeEnum), nullable=False)

    amount = Column(Float, nullable=False)
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    appointment = relationship("Appointment", backref="payments")

    def to_dict(self):
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "payment_type": self.payment_type.value,
            "status": self.status.value,
            "amount": self.amount,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<Payment #{self.id} Appointment:{self.appointment_id} {self.payment_type.value} {self.amount}>"