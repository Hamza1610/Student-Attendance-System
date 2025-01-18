from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends
from fastapi.responses import JSONResponse
from firebase_admin import auth
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import get_db
from app.models.student_model import Student
from PIL import Image
import torch
import numpy as np
import io
import json
import pickle
from psycopg2 import Binary
from app.utils.helpers import convert_embedding_to_base64, convert_base64_to_embedding
from app.utils.facenet import detect_faces, process_face_from_image

# FastAPI Router
router = APIRouter()

@router.post("/api/students/register")
def register_student(
    name: str = Form(...),
    student_id: str = Form(...),
    email: str = Form(...),
    class_name: str = Form(...),
    image: UploadFile = None,
    user_id: str = Form(..., description="Firebase UID of the admin/teacher"),
    db: Session = Depends(get_db)
):
    try:
        # Verify the admin/teacher from Firebase
        # user = auth.get_user(user_id)
        # if not user.email_verified:
        #     raise HTTPException(status_code=403, detail="Email not verified")

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

        # CHOOSE THE FIRES IMAGE FOR ONE PERSON EMBEDDING
        embedding = process_face_from_image(image_data)[0]

        # Convert list to bytes to save in database
        embedding = convert_embedding_to_base64(embedding)
        # Create a new student record and add to the database
        new_student = Student(
            name=name,
            student_id=student_id,
            email=email,
            class_name=class_name,
            face_embedding=embedding,
            registered_by=user_id  # Link the student to the admin/teacher
        )

        db.add(new_student)  # Add the new student to the session
        db.commit()  # Commit the transaction

        return {
            "message": "Student registered successfully",
            "student": {
                "name": name,
                "email": email,
                "classId": class_name
            }
        }

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/students")
def get_all_students(db: Session = Depends(get_db)):
    try:
        # Fetch all students from the database
        students = db.execute(select(Student)).scalars().all()
        
        # Check if students list is empty
        if not students:
            raise HTTPException(status_code=404, detail="No students found.")
        
        students_list = []
        # Convert each student to a dictionary if the to_dict method is defined
        for student in students:
            students_list.append(student.to_dict())
        
        print(students_list)
        return {"students": students_list}  # Return the list of students in JSON format
    
    except Exception as e:
        # Catch any errors and return a 500 internal server error
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/students/{id}")
def get_student_by_id(id: str, db: Session = Depends(get_db)):
    try:
        students = db.execute(
            select(Student).filter(Student.registered_by == id) # this is a query that is using  register_by to get all students
        ).scalars().all()

        print("Test ouput student:", students)
        if not students:
            raise HTTPException(status_code=404, detail="Student not found.")
        students_list = []
        # Convert each student to a dictionary if the to_dict method is defined
        for student in students:
            students_list.append(student.to_dict())
        
        return {"students": students_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/students/{id}")
async def update_student(
    name: str = Form(...),
    student_id: str = Form(...),
    email: str = Form(...),
    class_name: str = Form(...),
    registered_by: str = Form(...),
    face_embedding: UploadFile = None,
    db: Session = Depends(get_db),
):
    try:
        # Fetch the student to be updated
        student = db.execute(
            select(Student).filter(Student.student_id == id)
        ).scalars().first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        # Update the student record
        student.name = name
        student.student_id = student_id
        student.email = email
        student.class_name = class_name
        student.registered_by = registered_by

        if face_embedding:
            image_binary = await face_embedding.read()  # Save image as binary data
            embedding = process_face_from_image(image_binary)[0]
            student.face_embedding = embedding
        db.commit()  # Commit the changes
        return {"message": "Student updated successfully", "student": student.to_dict()}
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/students/{id}")
def delete_student(id: str, db: Session = Depends(get_db)):
    try:
        student = db.execute(
            select(Student).filter(Student.student_id == id)
        ).scalars().first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        db.delete(student)  # Delete the student from the session
        db.commit()  # Commit the transaction
        return {"message": "Student deleted successfully"}
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/students/face/{id}")
def register_face(
    id: str, # before was a form, need to be edited on the fronetend to meet this
    image: UploadFile = None,
    db: Session = Depends(get_db)
):
    try:
    # Check if student exists in the database
        student = db.execute(
            select(Student).filter(Student.student_id == id)
        ).scalars().first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        # Process the uploaded image
        if not image:
            raise HTTPException(status_code=400, detail="Image is required for face registration.")
        
        # Read the image data
        image_data = image.file.read()

        # Process face embedding from the image
        embedding = process_face_from_image(image_data)

        if not embedding:
            raise HTTPException(status_code=400, detail="No face detected in the image.")

        # Extract the first embedding (assuming you are only dealing with one face per image)
        embedding = embedding[0]

        # Convert the embedding to base64 format for storage
        embedding_base64 = convert_embedding_to_base64(embedding)
        # Save the base64 encoded embedding in the student's record
        student.face_embedding = embedding_base64  # Correct the field name if needed
        db.add(student)
        # Commit the changes to the database
        db.commit()

        return {"message": "Student face registered successfully."}
    
    except Exception as e:
        db.rollback()  # Rollback in case of any failure
        raise HTTPException(status_code=500, detail=str(e))
