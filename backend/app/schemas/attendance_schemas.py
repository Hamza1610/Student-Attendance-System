from pydantic import BaseModel
from datetime import date

class AttendanceSchema(BaseModel):
    class_id: str
    date: date
    student_id: str
    status: str

    class Config:
        from_attributes = True

class AttendanceBulkSchema(BaseModel):
    attendance: list[AttendanceSchema]

    class Config:
        from_attributes = True
