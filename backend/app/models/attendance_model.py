from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    student_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
