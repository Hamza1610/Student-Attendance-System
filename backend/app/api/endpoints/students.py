from fastapi import APIRouter, HTTPException, Form, UploadFile
from fastapi.responses import JSONResponse
from firebase_admin import auth
from app.db.collections import student_model
# from app.schemas.student_schemas import StudentBase
from PIL import Image
from facenet_pytorch import InceptionResnetV1
import torch
import numpy as np
import io
import base64

# FaceNet Model Setup
model = InceptionResnetV1(pretrained='vggface2').eval()

# FastAPI Router
router = APIRouter()

@router.post("/api/students")
async def register_student(
    name: str = Form(...),
    student_id: str = Form(...),
    email: str = Form(...),
    classId: str = Form(...),
    image: UploadFile = None,
    user_id: str = Form(...)
):
    try:
        # Verify the admin/teacher from Firebase
        user = auth.get_user(user_id)
        if not user.email_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        # Check if email already exists
        existing_student = student_model.find_by_email(student_email=email)
        if existing_student:
            raise HTTPException(status_code=400, detail="Student already registered")

        # Process the image
        if not image:
            raise HTTPException(status_code=400, detail="Image is required for FaceNet registration.")
        
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data)).resize((160, 160))  # Resize for FaceNet
        img_array = np.array(pil_image) / 255.0  # Normalize image
        if img_array.shape != (160, 160, 3):
            raise HTTPException(status_code=400, detail="Image must be RGB and of size 160x160.")

        # Get FaceNet embeddings
        img_tensor = np.transpose(img_array, (2, 0, 1))  # Convert to CHW format
        # Convert image to FaceNet input from numopy to flatten image to list
        embeddings = model(torch.tensor([img_tensor]).float()).detach().numpy().flatten().tolist()

        # Insert the student into MongoDB
        new_student = {
            "name": name,
            "studentId": student_id,
            "email": email,
            "classId": classId,
            "faceEmbedding": embeddings,
            "registeredBy": user_id  # Link the student to the admin/teacher
        }
        # Insert student data to collention
        student_model.create(data=new_student)

        return {
            "message": "Student registered successfully",
            "student": {
                "name": name,
                "email": email,
                "classId": classId
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/api/students")
async def get_all_students():
    try:
        students = list(student_model.find_all())  # Excluding the _id
        if not students:
            raise HTTPException(status_code=404, detail="No students found.")
        return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/students/{id}")
async def get_student_by_id(id: str):
    try:
        student = student_model.find_by_id(student_id=id)  # Fetch by email (or ID)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")
        return {"student": student}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Update student data
@router.put("/api/students/{id}")
async def update_student(id: str, student_data: dict):
    try:
        updated_student = student_model.update(
            student_id=id,
            data=student_data.model_dump()
        )
        if not updated_student:
            raise HTTPException(status_code=404, detail="Student not found.")
        
        return {"message": "Student updated successfully", "student": updated_student}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Delete student from class
@router.delete("/api/students/{id}")
async def delete_student(id: str):
    try:
        deleted_student = student_model.delete(student_id=id)
        if not deleted_student:
            raise HTTPException(status_code=404, detail="Student not found.")
        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/api/students/face")
async def register_face(
    student_email: str = Form(...),
    image: UploadFile = None
):
    try:
        # Check if student exists in the database
        student = student_model.find_by_email(student_email= student_email)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        # Process the uploaded image
        if not image:
            raise HTTPException(status_code=400, detail="Image is required for face registration.")
        
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data)).resize((160, 160))  # Resize image for FaceNet
        img_array = np.array(pil_image) / 255.0  # Normalize image
        if img_array.shape != (160, 160, 3):
            raise HTTPException(status_code=400, detail="Image must be RGB and of size 160x160.")

        # Get FaceNet embeddings
        img_tensor = np.transpose(img_array, (2, 0, 1))  # Convert to CHW format
        embeddings = model(torch.tensor([img_tensor]).float()).detach().numpy().flatten().tolist()

        # Save the face embeddings to the student's record in the database
        student_model.update(
            student_id= student_email,
            data={"faceEmbedding": embeddings}
        )

        return {"message": "Face registered successfully for student", "student": student_email}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
