from sqlalchemy import Column, String, Integer
from app.db.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True)
    user_id = Column(String, unique=True) # Firebase UID
    email = Column(String, unique=True)
    role = Column(String)  # 'teacher',    # Add relationships or other fields as necessary
    # Relationship to the classes they manage
    # classes = relationship("Class", back_populates="teacher_id") 'admin', etc.
    photo_url = Column(String, nullable=True)  # URL to the profile picture

