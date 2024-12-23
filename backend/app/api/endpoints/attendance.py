from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_student_attendance(student_id: str):
    pass