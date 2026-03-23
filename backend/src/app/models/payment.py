from app.db.db import db
from .status import PaymentStatusEnum

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))

    status = db.Column(PaymentStatusEnum)
    payment_date = db.Column(db.DateTime)

    consultation_fee = db.Column(db.Float)
    medicine_fee = db.Column(db.Float)
    total_amount = db.Column(db.Float)