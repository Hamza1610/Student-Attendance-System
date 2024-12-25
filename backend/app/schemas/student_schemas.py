from pydantic import BaseModel, EmailStr, Field
from typing import Optional
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


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    class_id: str  # Reference to the class ID


class StudentCreate(StudentBase):
    photo_url: str  # URL or base64-encoded string of the student's photo


class StudentUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    class_id: Optional[str]
    photo_url: Optional[str]


class StudentResponse(StudentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    photo_url: str  # The actual image URL for recognition

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
