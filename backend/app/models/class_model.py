from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Date, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
from datetime import datetime


class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, default=datetime.utcnow)
    end_date = Column(Date, nullable=True)
    status = Column(String, default="active")  # e.g., 'active', 'inactive'

    # Foreign key linking to the coordinator (Teacher/Admin)
    teacher_id = Column(String, ForeignKey("users.user_id"))
    
    # Relationship to the coordinator (Teacher/Admin)
    # coordinator = relationship("User", back_populates="classes")
