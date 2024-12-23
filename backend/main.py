from fastapi import FastAPI
import uvicorn
from app.api.endpoints import user, attendance, auth, students
from app.api.websockets import attendance_ws


app = FastAPI()


app.add_api_route(user.router, 'user')
app.add_api_route(auth.router, 'auth')
app.add_api_route(attendance.router, 'attendance')
app.add_api_route(students.router, 'stutents')
app.add_websocket_route(attendance_ws.router, 'ws')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Attendance System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)