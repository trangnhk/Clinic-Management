import hashlib
from sqlalchemy import event
import re
from app.models.users import User, Doctor, Patient
from app.db.db import db
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def check_password(password, hash):
    return check_password_hash(hash, password)

def register_user(username, email, password):
    if not username or not email or not password:
        raise Exception("Missing required fields")

    if User.query.filter_by(username=username).first():
        raise Exception("Username already exists")

    if User.query.filter_by(email=email).first():
        raise Exception("Email already exists")
    
    if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        raise Exception("Invalid email")

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role="PATIENT"
    )
    db.session.add(user)
    db.session.commit()
    return user

def login_user(username, password):
    user = User.query.filter_by(username=username).first()

    if not user:
        return None
    if not check_password(password, user.password_hash):
        return None
    if not user.is_active:
        raise Exception("User is inactive")

    return user

@event.listens_for(User, 'after_insert')
def create_profile(mapper, connection, target):
    if target.role == "DOCTOR":
        connection.execute(
            Doctor.__table__.insert(),
            {"user_id": target.id}
        )
    elif target.role == "PATIENT":
        connection.execute(
            Patient.__table__.insert(),
            {"user_id": target.id}
        )