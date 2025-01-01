from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
from datetime import datetime


class Class(Base):
    __tablename__ = "classes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")  # e.g., 'active', 'inactive'

    # Foreign key linking to the coordinator (Teacher/Admin)
    coordinator_id = Column(String, ForeignKey("users.id"))
    
    # Relationship to the coordinator (Teacher/Admin)
    coordinator = relationship("User", back_populates="classes")
