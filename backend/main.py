from fastapi import FastAPI
import uvicorn
from app.api.endpoints import user, attendance, auth, students
from app.api.websockets import attendance_ws


app = FastAPI()


app.include_router(user.router, prefix='/user', tags=['User']) # user related route such as 

app.include_router(auth.router, prefix='/auth', tags=['Authentication'])
app.include_router(attendance.router, prefix='/attendance', tags=['Attendance'])
app.include_router(students.router, prefix='/stutents', tags=['Students'])
# app.include_router(attendance_ws.router, prefix='/ws', tags=['Websockets'])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Attendance System"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)