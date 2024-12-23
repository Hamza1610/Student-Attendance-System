from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_auth_state(user_token: str): # since firebase is used to auth token is needed from user
    pass