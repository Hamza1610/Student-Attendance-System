from fastapi import APIRouter, HTTPException, Query, Form, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import get_db  # Assuming there's a utility to get DB session
from app.models.attendance_model import Attendance  # Assuming the SQLAlchemy model is in app.models
from app.schemas.attendance_schemas import AttendanceSchema, AttendanceBulkSchema

# FastAPI Router
router = APIRouter()

@router.get("/api/attendance", response_model=AttendanceBulkSchema)
def get_attendance(
    date: str = Query(None, description="Filter by date (YYYY-MM-DD)"),
    classId: str = Query(None, description="Filter by class ID"),
    studentId: str = Query(None, description="Filter by student ID"),
    db: Session = Depends(get_db)  # Inject DB session using Depends
):
    """
    Fetch attendance records with optional filtering by date, class ID, or student ID.
    """
    try:
        filters = {}
        if date:
            filters["date"] = date
        if classId:
            filters["class_id"] = classId
        if studentId:
            filters["student_id"] = studentId
        
        # Build dynamic query using filters
        result = db.execute(select(Attendance).filter_by(**filters))
        attendance_records = result.scalars().all()

        if not attendance_records:
            raise HTTPException(status_code=404, detail="No attendance records found.")

        # I assume you have a Pydantic schema for the response, I'm using skeleton here
        return {"attendance": attendance_records}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/attendance/")
def get_attendance_by_id(
    attendance_date: str = Query(None, description="Filter by date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)):
    """
    Fetch details of a specific attendance record by Date.
    """
    try:
        result = db.execute(select(Attendance).filter(Attendance.date == attendance_date))
        attendance = result.scalars().first()
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found.")
        # I assume you have a Pydantic schema for the response, I'm using skeleton here
        return {"attendance": attendance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/attendance")
def record_attendance(
    classId: str = Form(..., description="Class ID"),
    date: str = Form(..., description="Attendance date (YYYY-MM-DD)"),
    studentIds: list[str] = Form(..., description="List of student IDs"),
    status: str = Form(..., description="Attendance status (e.g., present, absent)"),
    db: Session = Depends(get_db)
):
    """
    Record attendance for a class or specific students.
    """
    try:
        studentIds = studentIds[0].split(",")

        # Create attendance records for multiple students
        attendance_records = []
        for student_id in studentIds:
            attendance = Attendance(
                class_id=classId,
                date=date,
                student_id=student_id,
                status=status
            )
            attendance_records.append(attendance)
        
        # Add and commit records
        db.add_all(attendance_records)
        db.commit()  # Commit all records to the database
        
        return {"message": "Attendance recorded successfully", "data": AttendanceBulkSchema(attendance=attendance_records)}
    
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/attendance/{id}")
def update_attendance(
    id: str,
    status: str = Form(..., description="Updated attendance status"),
    db: Session = Depends(get_db)
):
    """
    Update the attendance status of a specific record by Student ID.
    """
    try:
        result = db.execute(select(Attendance).filter(Attendance.student_id == id))
        attendance = result.scalars().first()
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found.")
        
        attendance.status = status
        db.commit()  # Commit the update
        # I assume you have a Pydantic schema for the response, I'm using skeleton here
        return {"message": "Attendance updated successfully", "attendance": attendance}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/attendance/{id}")
def delete_attendance(id: str, db: Session = Depends(get_db)):
    """
    Delete a specific attendance record by ID.
    """
    try:
        result = db.execute(select(Attendance).filter(Attendance.student_id == id))
        attendance = result.scalars().first()
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found.")
        
        db.delete(attendance)
        db.commit()  # Commit the deletion
        
        return {"message": "Attendance record deleted successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))