from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.class_model import Class
from app.schemas.class_schemas import ClassCreate, ClassRead, ClassUpdate
from app.crud.class_crud import ClassRepository
from app.db.base import get_db
from typing import List

# FastAPI Router
router = APIRouter()

@router.post("/api/classes", response_model=ClassRead)
async def create_class(
    class_obj: ClassCreate, db: AsyncSession = Depends(get_db)
):
    try:
        new_class = Class(
            name=class_obj.name,
            description=class_obj.description,
            start_date=class_obj.start_date,
            end_date=class_obj.end_date,
            status=class_obj.status
        )
        created_class = await ClassRepository(db).create_class(new_class)
        return created_class
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/classes", response_model=List[ClassRead])
async def get_all_classes(db: AsyncSession = Depends(get_db)):
    try:
        classes = await ClassRepository(db).get_all_classes()
        if not classes:
            raise HTTPException(status_code=404, detail="No classes found.")
        return classes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/classes/{id}", response_model=ClassRead)
async def get_class_by_id(id: str, db: AsyncSession = Depends(get_db)):
    try:
        class_obj = await ClassRepository(db).get_class_by_id(id)
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found.")
        return class_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/classes/{id}", response_model=ClassRead)
async def update_class(
    id: str, class_data: ClassUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        updated_class = await ClassRepository(db).update_class(id, class_data.dict())
        if not updated_class:
            raise HTTPException(status_code=404, detail="Class not found.")
        return updated_class
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/classes/{id}")
async def delete_class(id: str, db: AsyncSession = Depends(get_db)):
    try:
        deleted_class = await ClassRepository(db).delete_class(id)
        if not deleted_class:
            raise HTTPException(status_code=404, detail="Class not found.")
        return {"message": "Class deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
