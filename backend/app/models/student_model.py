from bson import ObjectId
from pydantic import EmailStr
from pymongo.collection import Collection

class StudentModel:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, data: dict):
        """Insert a new student into the collection."""
        result = self.collection.insert_one(data)
        return self.collection.find_one({"_id": result.inserted_id})

    def find_all(self):
        """Fetch all students."""
        return list(self.collection.find())

    def find_by_id(self, student_id: str):
        """Fetch a specific student by ID."""
        if not ObjectId.is_valid(student_id):
            return None
        return self.collection.find_one({"_id": ObjectId(student_id)})
    
    def find_by_email(self, student_email: str):
        """Fetch a specific student by ID."""
        if not student_email:
            return None
        return self.collection.find_one({"email": student_email})

    def update(self, student_id: str, data: dict):
        """Update a student's details."""
        if not ObjectId.is_valid(student_id):
            return None
        self.collection.update_one({"_id": ObjectId(student_id)}, {"$set": data})
        return self.collection.find_one({"_id": ObjectId(student_id)})

    def delete(self, student_id: str):
        """Delete a student by ID."""
        if not ObjectId.is_valid(student_id):
            return None
        self.collection.delete_one({"_id": ObjectId(student_id)})
        return {"message": "Student deleted"}
