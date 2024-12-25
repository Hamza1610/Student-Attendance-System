from pymongo.collection import Collection
from bson import ObjectId


class ClassModel:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, data: dict):
        """Insert a new class into the collection."""
        result = self.collection.insert_one(data)
        return self.collection.find_one({"_id": result.inserted_id})

    def find_all(self):
        """Fetch all classes."""
        return list(self.collection.find())

    def find_by_id(self, class_id: str):
        """Fetch a specific class by ID."""
        if not ObjectId.is_valid(class_id):
            return None
        return self.collection.find_one({"_id": ObjectId(class_id)})

    def update(self, class_id: str, data: dict):
        """Update a class's details."""
        if not ObjectId.is_valid(class_id):
            return None
        self.collection.update_one({"_id": ObjectId(class_id)}, {"$set": data})
        return self.collection.find_one({"_id": ObjectId(class_id)})

    def delete(self, class_id: str):
        """Delete a class by ID."""
        if not ObjectId.is_valid(class_id):
            return None
        self.collection.delete_one({"_id": ObjectId(class_id)})
        return {"message": "Class deleted"}
