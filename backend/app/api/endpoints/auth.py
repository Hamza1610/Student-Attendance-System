from fastapi import APIRouter, Depends
from firebase_admin import auth

router = APIRouter()

@router.get("/api/auth/me")
async def get_profile(user_id: str):
    try:
        # Fetch user from Firebase Authentication
        user = auth.get_user(user_id)
        if not user:
            return {
                "error": "User is not verified"
            }
        
        return {
            "uid": user.uid,
            "displayName": user.display_name,
            "email": user.email,
            "photoURL": user.photo_url,
            "emailVerified": user.email_verified,
            "phoneNumber": user.phone_number,
        }
    except Exception as e:
        return {"error": str(e)}
