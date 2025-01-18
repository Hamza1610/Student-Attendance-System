import React, { createContext, useState, useContext } from 'react';
import apiClient from '../services/api';
import { getUserIdFromCookie } from '../services/auth.service';


// Create AttendanceContext
const AttendanceContext = createContext();

// Provider component
export const AttendanceProvider = ({ children }) => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch classes
  const fetchClasses = async () => {
    console.log("Hey");
    
    try {
      const id = getUserIdFromCookie()
      const response = await apiClient.get(`/api/classes/${id}`) // fetch with id
      const classes_data  = response.data.classes
      console.log('Classes data:', classes_data);
      
      if (classes_data.length === 0) {
        setError('No classes found.');
      }
      
      if (classes_data.length >= 1) setClasses(classes_data);
      
    } catch (err) {
      setError(`Failed to fetch classes. ${err}`);
    } finally {
      setLoading(false);
    }
  };

  // Update student attendance
  const updateStudentAttendance = async (id, updatedData) => {
    try {
        // to implement api call later
        await apiClient.put(`/api/classes/${id}`, updatedData);

    } catch (error){
        // update table
        setError('Failed to update student attendance');
        console.log(error);
        
    }
  };



  return (
    <AttendanceContext.Provider value={{ classes, loading, error, fetchClasses, updateStudentAttendance }}>
      {children}
    </AttendanceContext.Provider>
  );
};

// Custom hook to use context
export const useAttendance = () => useContext(AttendanceContext);
