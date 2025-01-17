from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey, BLOB, LargeBinary
from sqlalchemy.orm import relationship
from app.utils.helpers import convert_embedding_to_base64, convert_base64_to_embedding

from app.db.base import Base
import json

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    student_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    class_name = Column(String)
    face_embedding = Column(Text, nullable=True)  # Change from ARRAY to BLOB
    registered_by = Column(String)

    def to_dict(self):
        """Converts the Student object to a dictionary."""
        
        return {
            'id': self.id,
            'name': self.name,
            'student_id': self.student_id,
            'email': self.email,
            'class_name': self.class_name,
            'face_embedding': convert_base64_to_embedding(self.face_embedding),
            'registered_by': self.registered_by,
        }

    def to_json(self):
        """Converts the Student object to a JSON string."""
        return json.dumps(self.to_dict())

