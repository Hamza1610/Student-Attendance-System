from fastapi import APIRouter

router = APIRouter()

@router.websocket('/')
def mark_attendance(data: list):
    pass