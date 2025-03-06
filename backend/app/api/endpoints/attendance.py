from fastapi import APIRouter, HTTPException, Query, UploadFile, Form, Depends, File
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import get_db 
from app.models.attendance_model import Attendance
from app.models.student_model import  Student 
from app.schemas.attendance_schemas import AttendanceSchema, AttendanceBulkSchema
from app.utils.helpers import convert_embedding_to_base64, convert_base64_to_embedding
from app.utils.facenet import detect_faces, process_face_from_image, detect_faces, process_image
import numpy as np


# FastAPI Router
router = APIRouter()

@router.get("/api/attendance", response_model=AttendanceBulkSchema)
def get_attendance(
    date: str = Query(None, description="Filter by date (YYYY-MM-DD)"),
    className: str = Query(None, description="Filter by class ID"),
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
        if className:
            filters["class_name"] = className
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
    className: str = Form(..., description="Class Name is used here instead of class ID"),
    date: str = Form(..., description="Attendance date (YYYY-MM-DD)"),
    image: UploadFile = File(..., description="Uploaded face image"),
    db: Session = Depends(get_db)
):
    """
    Process the uploaded image, compare it with stored embeddings, and mark attendance if a match is found.
    """
    try:
        print(f"Processing attendance for class {className} on {date} using {image}")
        # Extract face embeddings from the uploaded image
        detected_embeddings = process_image(image)
        if not detected_embeddings:
            raise HTTPException(status_code=400, detail="No face detected in the image.")

        students = db.query(Student).filter(Student.class_name == className).all()

        print(f"Processing attendance for {len(students)} students in class {className}")
        
        if not students:
            raise HTTPException(status_code=404, detail="No students found for this class.")
        
        recognized_students = []
        for student in students:
            stored_embedding = convert_base64_to_embedding(student.face_embedding)
            stored_embedding = np.array(stored_embedding)  # Convert list to NumPy array

            for detected_embedding in detected_embeddings:

                detected_embedding = np.array(detected_embedding)  # Convert list to NumPy array
                similarity_score = np.linalg.norm(stored_embedding - detected_embedding)
                print(f"Similarity score for {student.id}: {similarity_score}")

                if similarity_score > 0.6:  # Threshold for recognition (higher is better)
                    recognized_students.append(student.id)
                    break  # Stop checking if at least one match is found
        if not recognized_students:
            return {"message": "No recognized faces matched with stored embeddings."}
        
        # Create attendance records
        attendance_records = []
        for student_id in recognized_students:
            attendance_objs = db.query(Attendance).filter_by(
                student_id=str(student_id), date=date, status="present"
            ).all()

            if attendance_objs:
                print(f"Attendance already recorded for student {student_id}")
                continue

            attendance = Attendance(
                class_name=className,
                date=date,
                student_id=str(student_id),
                status="present"
            )
            attendance_records.append(attendance)
        
        print(f"Attendance records to be added: {len(attendance_records)}")
        
        if not attendance_records:
            return {"message": "Attendance already recorded for all recognized students."}
        
        db.add_all(attendance_records)
        db.commit()
        
        return {"message": "Attendance recorded successfully", "recognized_students": recognized_students}
    
    except Exception as e:
        db.rollback()
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