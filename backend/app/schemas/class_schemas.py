from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic schema for creating a new class
class ClassCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = "active"  # Default to "active"
    coordinator_id: str  # Foreign key linking to the coordinator (Teacher/Admin)

# Pydantic schema for reading a class (with ID)
class ClassRead(ClassCreate):
    id: str
    coordinator_id: str
    coordinator_name: str  # Include the name of the coordinator

    class Config:
        from_attributes = True

# Pydantic schema for updating a class
class ClassUpdate(ClassCreate):
    pass
