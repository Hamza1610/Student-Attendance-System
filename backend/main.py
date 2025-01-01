from fastapi import FastAPI
import uvicorn
from app.api.endpoints import user, attendance, auth, students, classes
from app.models import Base
from app.db.base import engine
from app.utils.firebase import initalize_firebase_admin


# Initialize Firebase Admin SDK
initalize_firebase_admin()


app = FastAPI()


# Include your routers
app.include_router(auth.router, prefix='/v1', tags=['Authentication'])
app.include_router(attendance.router, prefix='/v1', tags=['Attendance'])
app.include_router(classes.router, prefix='/v1', tags=['Class'])
app.include_router(students.router, prefix='/v1', tags=['Students'])
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Attendance System"}

# Create tables on startup (migrations are better for production)
@app.on_event("startup")
def startup_event():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)