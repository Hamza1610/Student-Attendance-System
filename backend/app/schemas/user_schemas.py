from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    email: str
    role: str
    photo_url: str | None  # The profile picture URL, it could be None if not set
