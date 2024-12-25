from typing import Optional
from pydantic import BaseModel, Field

class ClassBase(BaseModel):
    name: str
    description: Optional[str]


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class ClassResponse(ClassBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
