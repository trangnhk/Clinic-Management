from app.db.db import db
from enum import Enum

class RoleEnum(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class SlotStatusEnum(str, Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    BLOCKED = "BLOCKED"

class AppointmentStatusEnum(str, Enum):
    WAITING_EXAMINATION = "WAITING_EXAMINATION"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PENDING_RESULT = "PENDING_RESULT"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class TestStatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class PaymentTypeEnum(str,Enum):
    DEPOSIT = "DEPOSIT"
    FINAL = "FINAL"
    MEDICINE = "MEDICINE"
    LAB_TEST = "LAB_TEST"

class PaymentStatusEnum(str,Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    # REFUNDED = "REFUNDED"