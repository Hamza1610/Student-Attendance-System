# Student Attendance System Using Face Recognition

A real-time attendance tracking system powered by facial recognition technology, built with React, FastAPI, MongoDB, and FaceNet.

## Features

- Real-time face detection and recognition for attendance tracking
- Secure user authentication and authorization
- Student profile management with facial data
- Comprehensive attendance reporting and analytics
- Real-time processing using WebSocket communication
- Intuitive dashboard with attendance statistics
- Customizable system settings and configurations

## Tech Stack

### Frontend
- React.js
- HTML5/CSS3
- WebSocket client for real-time communication
- Firebase

### Backend
- FastAPI (Python)
- FaceNet for facial recognition
- WebSocket server for real-time processing
- JWT authentication

### Database
- MongoDB for data persistence

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MongoDB (v4.4 or higher)
- Webcam or camera device for face detection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Hamza1610/Student-Attendance-System.git
cd Student-Attendance-System
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Install backend dependencies:
```bash
cd ../backend
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws

# Backend (.env)
MONGODB_URI=mongodb://localhost:27017/attendance
JWT_SECRET=your_jwt_secret
```

5. Start MongoDB service on your machine

## Running the Application

1. Start the backend server:
```bash
cd backend

py main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the application at `http://localhost:3000`

## Project Structure

```
attendance-system/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── public/
├── backend/
│   ├── modules/
│   │   ├── auth/
│   │   ├── students/
│   │   └── attendance/
│   ├── models/
│   └── utils/
└── docs/
```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Register new admin user

### Student Management
- `POST /api/students` - Add new student
- `GET /api/students` - List all students
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student information
- `DELETE /api/students/{id}` - Remove student

### Attendance Management
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance` - Get attendance records
- `GET /api/attendance/report` - Generate attendance report

## WebSocket Endpoints

- `/ws/attendance` - Real-time face recognition and attendance tracking

## Security

- JWT-based authentication
- Secure password hashing
- Rate limiting on API endpoints
- Input validation and sanitization
- CORS configuration

## Configuration

System settings can be configured through the admin dashboard:
- Face recognition confidence threshold
- Attendance time window
- Session timeout
- Maximum retry attempts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and queries, please open an issue in the GitHub repository or contact the development team.

## Future Enhancements

- Multi-language support
- Offline mode capability
- Additional biometric authentication methods
- Advanced analytics and reporting features
- Mobile application support