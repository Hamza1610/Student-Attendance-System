import React, { createContext, useState, useContext, useRef } from 'react';
import apiClient from '../services/api';
import { getUserIdFromCookie } from '../services/auth.service';
import { clearDetectedFaces } from '../services/attendance.service';

// Create AttendanceContext
const AttendanceContext = createContext();

// Provider component
export const AttendanceProvider = ({ children }) => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const markAttendance = async (classDetail, detections, webcamRef) => {
    console.log("From Context MarkAttendance: ", {
      classDetail,
      detections,
      webcamRef: webcamRef.current
    });
  
    // Check if webcam is ready
    if (!webcamRef.current || webcamRef.current.video?.readyState !== 4) {
      console.error("Webcam is not ready yet");
      return;
    }
  
    // Check if getScreenshot function exists
    if (typeof webcamRef.current.getScreenshot !== 'function') {
      console.error("getScreenshot method is not available");
      return;
    }
  
    try {
      const imageSrc = webcamRef.current?.getScreenshot();
      if (!imageSrc) {
        console.error("Failed to capture screenshot");
        return;
      }
  
      console.log("Screenshot captured successfully:", imageSrc.substring(0, 50) + "...");
      clearDetectedFaces("webcam-div");
      
      // Convert base64 to blob
      const blob = await fetch(imageSrc).then(res => res.blob());
  
      // Debug detections
      console.log("Raw detections received:", JSON.stringify(detections, null, 2));
  
      // Validate and filter out invalid detections
      // const validDetections = detections.filter(detection => {
      //   if (!detection || !detection.box) {
      //     console.warn("Skipping invalid detection:", detection);
      //     return false;
      //   }
  
      //   const { x, y, width, height } = detection.box;
      //   if (x == null || y == null || width == null || height == null) {
      //     console.warn("Skipping detection with null bounding box:", detection.box);
      //     return false;
      //   }
  
      //   return true;
      // });
  
      // if (validDetections.length === 0) {
      //   console.error("No valid face detections found. Aborting attendance marking.");
      //   return;
      // }
  
      // console.log("Valid detections:", validDetections);
  
      // Create a FormData payload
      const formData = new FormData();
      formData.append("className", classDetail.name);
  
      // Use current date in YYYY-MM-DD format
      const today = new Date().toISOString().split("T")[0];
      formData.append("date", today);
      formData.append("image", blob, "attendance.jpg");
  
      try {
        // Send to FastAPI
        const response = await apiClient.post("/api/attendance", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
  
        if (response.status === 200) {
          console.log('Student attendance updated successfully:', response.data);
          // return validDetections;
        }
      } catch (error) {
        setError("Failed to mark attendance. Please try again.");
        console.error("Error marking attendance:", error.response ? error.response.data : error.message);
      }
    } catch (error) {
      console.error("Error capturing screenshot:", error);
    }
  };
  
  

  
  // Fetch classes
  const fetchClasses = async () => {
    console.log("Fetching classes...");
    
    try {
      const id = getUserIdFromCookie();
      if (!id) {
        setError("User ID not found in cookies.");
        return;
      }

      const response = await apiClient.get(`/api/classes/${id}`);
      const classes_data = response.data.classes;
      console.log('Classes data:', classes_data);
      
      if (!classes_data || classes_data.length === 0) {
        setError('No classes found.');
        setClasses([]);
      } else {
        setClasses(classes_data);        
      }
    } catch (err) {
      setError(`Failed to fetch classes. ${err.response ? err.response.data : err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Update student attendance
  const updateStudentAttendance = async (id, updatedData) => {
    try {
      await apiClient.put(`/api/classes/${id}`, updatedData);
      fetchClasses(); // Refresh class list
    } catch (error) {
      setError(`Failed to update student attendance: ${error.response ? error.response.data : error.message}`);
    }
  };

  return (
    <AttendanceContext.Provider value={{
      classes,
      loading,
      error,
      setError,
      fetchClasses,
      updateStudentAttendance,
      markAttendance
    }}>
      {children}
    </AttendanceContext.Provider>
  );
};

// Custom hook to use context
export const useAttendance = () => useContext(AttendanceContext);
