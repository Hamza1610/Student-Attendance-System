from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, Optional
from bson import ObjectId


# Custom ObjectId handling for MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class AttendanceBase(BaseModel):
    date: datetime
    class_id: str
    student_ids: List[str]  # List of student IDs marked as present


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    date: Optional[datetime]
    student_ids: Optional[List[str]]


class AttendanceResponse(AttendanceBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
