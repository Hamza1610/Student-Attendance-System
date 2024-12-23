from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_user_profile(email: str):
    pass