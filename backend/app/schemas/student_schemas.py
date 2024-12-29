from pydantic import BaseModel
from typing import List, Optional

class StudentBase(BaseModel):
    name: str
    student_id: str
    email: str
    class_id: str
    face_embedding: Optional[List[float]] = None
    registered_by: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True
