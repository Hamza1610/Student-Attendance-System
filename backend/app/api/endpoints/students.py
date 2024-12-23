from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_student_info(student_id: str):
    pass