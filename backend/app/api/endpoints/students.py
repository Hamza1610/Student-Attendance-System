from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends
from fastapi.responses import JSONResponse
from firebase_admin import auth
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import get_db
from app.models.student_model import Student, Class  # Assuming 'Student' model is in app.models
from PIL import Image
from facenet_pytorch import InceptionResnetV1
import torch
import numpy as np
import io
import json

# FaceNet Model Setup
model = InceptionResnetV1(pretrained='vggface2').eval()

# FastAPI Router
router = APIRouter()

@router.post("/api/students")
def register_student(
    name: str = Form(...),
    student_id: str = Form(...),
    email: str = Form(...),
    class_id: str = Form(...),
    image: UploadFile = None,
    user_id: str = Form(..., description="Firebase UID of the admin/teacher"),
    db: Session = Depends(get_db)
):
    try:
        # Verify the admin/teacher from Firebase
        user = auth.get_user(user_id)
        if not user.email_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        # Check if email already exists
        existing_student = db.execute(
            select(Student).filter(Student.student_id == student_id)
        ).scalars().first()

        if existing_student:
            raise HTTPException(status_code=400, detail="Student already registered")

        # Process the image
        if not image:
            raise HTTPException(status_code=400, detail="Image is required for FaceNet registration.")
        
        image_data = image.file.read()
        pil_image = Image.open(io.BytesIO(image_data)).resize((160, 160))  # Resize for FaceNet
        img_array = np.array(pil_image) / 255.0  # Normalize image
        if img_array.shape != (160, 160, 3):
            raise HTTPException(status_code=400, detail="Image must be RGB and of size 160x160.")

        # Get FaceNet embeddings
        img_tensor = np.transpose(img_array, (2, 0, 1))  # Convert to CHW format
        embeddings = model(torch.tensor([img_tensor]).float()).detach().numpy().flatten().tolist()

        # Convert list to JSON string before saving
        embeddings = json.dumps(embeddings)

        # Create a new student record and add to the database
        new_student = Student(
            name=name,
            student_id=student_id,
            email=email,
            class_id=class_id,
            face_embedding=embeddings,
            registered_by=user_id  # Link the student to the admin/teacher
        )

        db.add(new_student)  # Add the new student to the session
        db.commit()  # Commit the transaction

        return {
            "message": "Student registered successfully",
            "student": {
                "name": name,
                "email": email,
                "classId": class_id
            }
        }

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/students")
def get_all_students(db: Session = Depends(get_db)):
    try:
        students = db.execute(select(Student)).scalars().all()
        if not students:
            raise HTTPException(status_code=404, detail="No students found.")
        return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/students/{id}")
def get_student_by_id(id: str, db: Session = Depends(get_db)):
    try:
        student = db.execute(
            select(Student).filter(Student.id == id)
        ).scalars().first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")
        return {"student": student}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/students/{id}")
def update_student(id: str, student_data: dict, db: Session = Depends(get_db)):
    try:
        # Fetch the student to be updated
        student = db.execute(
            select(Student).filter(Student.id == id)
        ).scalars().first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        # Update the student record
        for key, value in student_data.items():
            setattr(student, key, value)

        db.commit()  # Commit the changes
        return {"message": "Student updated successfully", "student": student}
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/students/{id}")
def delete_student(id: str, db: Session = Depends(get_db)):
    try:
        student = db.execute(
            select(Student).filter(Student.id == id)
        ).scalars().first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        db.delete(student)  # Delete the student from the session
        db.commit()  # Commit the transaction
        return {"message": "Student deleted successfully"}
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/students/face")
def register_face(
    student_email: str = Form(...),
    image: UploadFile = None,
    db: Session = Depends(get_db)
):
    try:
        # Check if student exists in the database
        student = db.execute(
            select(Student).filter(Student.email == student_email)
        ).scalars().first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        # Process the uploaded image
        if not image:
            raise HTTPException(status_code=400, detail="Image is required for face registration.")
        
        image_data = image.file.read()
        pil_image = Image.open(io.BytesIO(image_data)).resize((160, 160))  # Resize image for FaceNet
        img_array = np.array(pil_image) / 255.0  # Normalize image
        if img_array.shape != (160, 160, 3):
            raise HTTPException(status_code=400, detail="Image must be RGB and of size 160x160.")

        # Get FaceNet embeddings
        img_tensor = np.transpose(img_array, (2, 0, 1))  # Convert to CHW format
        embeddings = model(torch.tensor([img_tensor]).float()).detach().numpy().flatten().tolist()

        # Update the student record with face embeddings
        student.face_embedding = json.dumps(embeddings)
        db.commit()  # Commit the changes

        return {"message": "Face registered successfully for student", "student": student_email}

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))
