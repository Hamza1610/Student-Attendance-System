from typing import List, Optional
from app.models.student import Student
from app.db.mongodb import MongoDB

class Students:
    def __init__(self, db: MongoDB):
        self.collection = db.get_collection("students")

    async def get_student_by_id(self, student_id: str) -> Optional[Student]:
        student_data = await self.collection.find_one({"_id": student_id})
        if student_data:
            return Student(**student_data)
        return None

    async def get_all_students(self) -> List[Student]:
        students_cursor = self.collection.find()
        students = await students_cursor.to_list(length=None)
        return [Student(**student_data) for student_data in students]

    async def create_student(self, student: Student) -> Student:
        await self.collection.insert_one(student.dict())
        return student