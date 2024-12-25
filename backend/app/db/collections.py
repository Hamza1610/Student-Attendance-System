from . import db # Import the db instance from the __init__.py file
from app.models import StudentModel, ClassModel, AttendanceModel, FaceRecognitionModel

# Initialize the student model
students_collection = db["students"]
student_model = StudentModel(students_collection)

# Initialize the class model
classes_collection = db["classes"]
class_model = ClassModel(classes_collection)

#Initialize the attendance model
attendance_collection = db["attendance"]
attendance_model = AttendanceModel(attendance_collection)

# Initialize the face recognition model
facerecognition_collection = db["face_recognition"]
facerecognition_model = FaceRecognitionModel(facerecognition_collection)
