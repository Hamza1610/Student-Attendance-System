from fastapi import APIRouter, HTTPException, Query, Form
from app.db.collections import attendance_model

# FastAPI Router
router = APIRouter()


@router.get("/api/attendance")
async def get_attendance(
    date: str = Query(None, description="Filter by date (YYYY-MM-DD)"),
    classId: str = Query(None, description="Filter by class ID"),
    studentId: str = Query(None, description="Filter by student ID")
):
    """
    Fetch attendance records with optional filtering by date, class ID, or student ID.
    """
    try:
        filters = {}
        if date:
            filters["date"] = date
        if classId:
            filters["classId"] = classId
        if studentId:
            filters["studentId"] = studentId
        
        attendance_records = list(attendance_model.find_all(query=filters))  # Exclude _id field
        if not attendance_records:
            raise HTTPException(status_code=404, detail="No attendance records found.")
        
        return {"attendance": attendance_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/attendance/{id}")
async def get_attendance_by_id(id: str):
    """
    Fetch details of a specific attendance record by ID.
    """
    try:
        attendance = attendance_model.find_by_id(attendance_id=id)  # Fetch by attendanceId
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found.")
        return {"attendance": attendance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/attendance")
async def record_attendance(
    classId: str = Form(..., description="Class ID"),
    date: str = Form(..., description="Attendance date (YYYY-MM-DD)"),
    studentIds: list[str] = Form(..., description="List of student IDs"),
    status: str = Form(..., description="Attendance status (e.g., present, absent)")
):
    """
    Record attendance for a class or specific students.
    """
    try:
        # Prepare attendance records for each student
        attendance_records = [
            {
                "classId": classId,
                "date": date,
                "studentId": studentId,
                "status": status,
            }
            for studentId in studentIds
        ]
        
        # Insert attendance records into MongoDB for many students
        attendance_model.create_all(attendance_records)
        return {"message": "Attendance recorded successfully", "attendance": attendance_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/attendance/{id}")
async def update_attendance(id: str, status: str = Form(..., description="Updated attendance status")):
    """
    Update the attendance status of a specific record by ID.
    """
    try:
        # Update attendance record by attendanceId
        updated_attendance = attendance_model.update(
            attendance_id=id, # Find by attendanceId
            data=status,  # Update only the status
        )
        if not updated_attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found.")
        return {"message": "Attendance updated successfully", "attendance": updated_attendance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/attendance/{id}")
async def delete_attendance(id: str):
    """
    Delete a specific attendance record by ID.
    """
    try:
        deleted_attendance = attendance_model.delete(attendance_id=id)   # Delete by attendanceId
        if not deleted_attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found.")
        return {"message": "Attendance record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
