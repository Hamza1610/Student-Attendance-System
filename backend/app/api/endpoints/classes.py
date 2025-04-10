from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.class_model import Class
from app.schemas.class_schemas import ClassCreate, ClassRead, ClassUpdate
from app.db.base import get_db
from typing import List
from firebase_admin import auth

# FastAPI Router
router = APIRouter()

@router.post("/api/classes")
def create_class(
    name: str = Form(..., description="Class name or Subject such as Math419"),
    description: str = Form(..., description="Class description"),
    start_date: str = Form(..., description="Class starting date in form of YYYY-MM-DD"),
    end_date: str = Form(..., description="Class ending date in form of YYYY-MM-DD"),
    status: str = Form(..., description="Class status (active or closed)"),
    teacher_id: str =Form(..., description="Temporal: Teatcher/Admin firebase Id(can be modify for better code"),
    db: Session = Depends(get_db)
):
    try:
        # Ensure teacher exists in Firebase
        try:
            auth.get_user(teacher_id)
        except Exception:
            raise HTTPException(status_code=404, detail="Teacher not found in Firebase")
        except:
            raise HTTPException(status_code=500, detail="No internet connection")
        # Convert the class_obj to a Form and teacher_id is to be faetched from the header
        # check if use_id is valid using firebase 
        new_class = Class(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
            teacher_id=teacher_id
        )
        db.add(new_class)  # Add the new class to the session
        db.commit()  # Commit the transaction
        db.refresh(new_class)  # Refresh to get the created class data
        return { "message": "Class created successfully" }
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/classes")
def get_all_classes(db: Session = Depends(get_db)):
    try:
        classes = db.execute(select(Class)).scalars().all()  # Get all classes
        return {"classes": classes if classes else []}
    
    except Exception as e:
        print('Error', e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/classes/{id}")
def get_class_by_id(id: str, db: Session = Depends(get_db)):
    
    try:
        class_objs = db.execute(
            select(Class).filter(Class.teacher_id == id)
        ).scalars().all()  # Fetch all matching classes

        print('Class Gotten', class_objs)
        return {"classes": class_objs if class_objs else []}
    except Exception as e:
        print('Error', e)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/classes/{id}") # this should be a form
def update_class(
    id: str, class_data: ClassUpdate, db: Session = Depends(get_db)
):
    try:
        class_obj = db.execute(
            select(Class).filter(Class.id == id)
        ).scalars().first()

        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found.")
        
        # Update the class object
        for key, value in class_data.dict().items():
            setattr(class_obj, key, value)

        db.commit()  # Commit the changes
        db.refresh(class_obj)  # Refresh to get the updated class data
        return class_obj
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/classes/{id}")
def delete_class(id: str, db: Session = Depends(get_db)):
    try:
        class_obj = db.execute(
            select(Class).filter(Class.id == id)
        ).scalars().first()

        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found.")
        
        db.delete(class_obj)  # Delete the class object
        db.commit()  # Commit the transaction
        return {"message": "Class deleted successfully"}
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))
