from sqlalchemy import Column, String, Integer, Date
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    student_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
