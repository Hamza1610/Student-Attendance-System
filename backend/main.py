from fastapi import FastAPI
import uvicorn
from app.api.endpoints import attendance, auth, students, classes
from app.models import Base
from app.db.base import engine
from app.utils.firebase import initalize_firebase_admin
from fastapi.middleware.cors import CORSMiddleware

# Initialize Firebase Admin SDK
initalize_firebase_admin()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include your routers
app.include_router(auth.router, tags=['Authentication'])
app.include_router(attendance.router, tags=['Attendance'])
app.include_router(classes.router, tags=['Class'])
app.include_router(students.router, tags=['Students'])


# Create tables on startup (migrations are better for production)
@app.on_event("startup")
def startup_event():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Attendance System"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)