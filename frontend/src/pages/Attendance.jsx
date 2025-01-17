import React, { useEffect, useState } from 'react';
import FaceRecognitionAttendance from '../components/attendance/AttendanceCamera';
import apiClient from '../services/api';
import { getUserIdFromCookie } from '../services/auth.service';
import '../styles/Attendance.css';
import AttendanceTable from '../components/attendance/AttendanceTable';
import { AttendanceProvider } from '../contexts/AttendanceContext';

const AttendanceTracking = () => {
  const [isCamara, setIsCamara] = useState(false);
  const [error, setError] = useState(null);
  const [classes, setClasses] = useState([]);

  const openCamera = () => {
  }
  const handleCancleCapture = () => {
  }

  return (
    <div className='attendance'>
      <AttendanceProvider>
        <AttendanceTable />
      </AttendanceProvider>
      {/* <h1>Attendance</h1>
      {error && (<div className='error-message'>{error}</div>)}
      {isCamara && (<FaceRecognitionAttendance />)}
      <div className="camera-actions">
        <button className="camera-btn" onClick={openCamera}>Open</button>
        <button className="camera-btn" onClick={handleCancleCapture}>Close</button>
      </div> */}
    </div>
  )
}
export default AttendanceTracking;
