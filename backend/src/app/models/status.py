from app.db.db import db

RoleEnum = db.Enum("PATIENT", "DOCTOR", "ADMIN", name="role_enum")
GenderEnum = db.Enum("MALE", "FEMALE", name="gender_enum")
SlotStatusEnum = db.Enum("AVAILABLE", "BOOKED", "BLOCKED", name="slot_status_enum")

AppointmentStatusEnum = db.Enum(
    "WAITING_EXAMINATION",
    "PENDING_PAYMENT",
    "PENDING_RESULT",
    "COMPLETED",
    name="appointment_status_enum"
)

PaymentStatusEnum = db.Enum("PENDING", "PAID", "FAILED", name="payment_status_enum")

TestStatusEnum = db.Enum("PENDING", "IN_PROGRESS", "DONE", name="test_status_enum")