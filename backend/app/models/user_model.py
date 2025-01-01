from sqlalchemy import Column, String
from app.db.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, index=True)  # Firebase UID
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)  # 'teacher', 'admin', etc.
    photo_url = Column(String, nullable=True)  # URL to the profile picture

    # Add relationships or other fields as necessary
    # Relationship to the classes they manage
    classes = relationship("Class", back_populates="coordinator")