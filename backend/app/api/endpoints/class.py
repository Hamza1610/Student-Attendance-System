from fastapi import APIRouter, HTTPException
from db.collections import class_model

# declare api router
router = APIRouter()

@router.get("/api/classes")
async def get_all_classes():
    try:
        classes = list(class_model.find_all())  # Exclude MongoDB _id
        if not classes:
            raise HTTPException(status_code=404, detail="No classes found.")
        return {"classes": classes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/classes/{id}")
async def get_class_by_id(id: str):
    try:
        class_details = class_model.find_by_id(class_id=id)  # Fetch by classId
        if not class_details:
            raise HTTPException(status_code=404, detail="Class not found.")
        return {"class": class_details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/classes")
async def add_class(class_data: dict):
    try:
        # Check if class already exists
        if class_model.find_by_id(class_id=class_data["classId"]):
            raise HTTPException(status_code=400, detail="Class already exists.")

        # Create new class into MongoDB
        class_model.create(data=class_data)
        return {"message": "Class added successfully", "class": class_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/classes/{id}")
async def update_class(id: str, class_data: dict):
    try:

        updated_class = class_model.update(class_id=id, data=class_data)

        if not updated_class:
            raise HTTPException(status_code=404, detail="Class not found.")
        return {"message": "Class updated successfully", "class": updated_class}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Delete specific class
@router.delete("/api/classes/{id}")
async def delete_class(id: str):
    try:
        deleted_class = class_model.delete(class_id=id)
        if not deleted_class:
            raise HTTPException(status_code=404, detail="Class not found.")
        return {"message": "Class deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


