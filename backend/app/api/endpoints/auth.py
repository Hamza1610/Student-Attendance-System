from fastapi import APIRouter, HTTPException, Depends
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user_model import User  # Assuming you have a User model
from app.schemas.user_schemas import UserProfile  # Define this schema for the response

router = APIRouter()

# Endpoint to register a Teacher/Admin and store their profile in the database
@router.post("/api/register-teacher/{user_id}")
def register_teacher(user_id: str, db: Session = Depends(get_db)):
    try:
        print("User test", user_id)
        # Fetch user data from Firebase
        user = auth.get_user(user_id)
        print("User", user)
        if not user.email_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        # Check if user already exists
        existing_user = db.query(User).filter(User.user_id == user.uid).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already registered")

        # Create a new User record and save it to the database
        new_user = User(
            user_id=user.uid,
            name=user.display_name,
            email=user.email,
            role="teacher",  # Or "admin", based on your logic
            photo_url=user.photo_url
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Ensure we have the updated object

        return {"message": "Teacher registered successfully", "user": new_user}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to fetch Teacher/Admin profile data
@router.get("/api/profile/{user_id}")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    try:
        # Fetch user data from Firebase
        try:
            firebase_user = auth.get_user(user_id)
        except FirebaseError:
            raise HTTPException(status_code=400, detail="Invalid user ID or Firebase error")

        # Check if the user exists in your database
        user_record = db.query(User).filter(User.user_id == firebase_user.uid).first()

        print("User record:", user_record)
        if not user_record:
            raise HTTPException(status_code=404, detail="User not found")

        # Return user profile details
        return {
            "name": user_record.name,
            "email": user_record.email,
            "role": user_record.role,
            "photo_url": user_record.photo_url
        }

    except HTTPException:
        raise  # Re-raise known exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
