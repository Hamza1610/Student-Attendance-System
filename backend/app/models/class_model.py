from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

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

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)  # e.g., 'admin', 'teacher'

    # Relationship to the classes they manage
    classes = relationship("Class", back_populates="coordinator")
