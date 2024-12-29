from sqlalchemy import Column, String, Integer, Date, ForeignKey, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    student_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    class_id = Column(String)
    face_embedding = Column(BLOB, nullable=True)  # Change from ARRAY to BLOB
    registered_by = Column(String)  