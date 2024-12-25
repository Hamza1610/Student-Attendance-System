from pymongo.collection import Collection
from bson import ObjectId

class AttendanceModel:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, data: dict):
        """Record attendance for a class or student(s)."""
        result = self.collection.insert_one(data)
        return self.collection.find_one({"_id": result.inserted_id})
    
    def create_all(self, data: list[dict]):
        """Record attendance for a class or students."""
        result = self.collection.insert_many(data)
        return self.collection.find({}, {"_id": result.inserted_ids})

    def find_all(self, query: dict = None):
        """Fetch attendance records (optionally filtered by date, class, or student)."""
        query = query or {}
        return list(self.collection.find(query))

    def find_by_id(self, attendance_id: str):
        """Fetch a specific attendance record by ID."""
        if not ObjectId.is_valid(attendance_id):
            return None
        return self.collection.find_one({"_id": ObjectId(attendance_id)})

    def update(self, attendance_id: str, data: dict):
        """Update an attendance record."""
        if not ObjectId.is_valid(attendance_id):
            return None
        self.collection.update_one({"_id": ObjectId(attendance_id)}, {"$set": data})
        return self.collection.find_one({"_id": ObjectId(attendance_id)})

    def delete(self, attendance_id: str):
        """Delete an attendance record by ID."""
        if not ObjectId.is_valid(attendance_id):
            return None
        self.collection.delete_one({"_id": ObjectId(attendance_id)})
        return {"message": "Attendance record deleted"}
