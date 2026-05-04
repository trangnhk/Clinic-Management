from app.db.db import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

class Specialization(db.Model):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text, nullable=True)

    doctors = relationship("Doctor", backref="specialization", lazy=True)
    
    def __str__(self):
        return self.name