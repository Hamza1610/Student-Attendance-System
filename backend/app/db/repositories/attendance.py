from bson.objectid import ObjectId
from base import Base

class Attendance:
    def __init__(self):
        super.__init__(self, Base)
        self.collection = self.db.get_collection("attendance")

    def add_attendance_record(self, student_id, date, status):
        attendance_record = {
            "student_id": student_id,
            "date": date,
            "status": status
        }
        result = self.collection.insert_one(attendance_record)
        return str(result.inserted_id)

    def get_attendance_record(self, record_id):
        return self.collection.find_one({"_id": ObjectId(record_id)})

    def update_attendance_record(self, record_id, status):
        result = self.collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {"status": status}}
        )
        return result.modified_count

    def delete_attendance_record(self, record_id):
        result = self.collection.delete_one({"_id": ObjectId(record_id)})
        return result.deleted_count

    def get_attendance_by_student(self, student_id):
        return list(self.collection.find({"student_id": student_id}))