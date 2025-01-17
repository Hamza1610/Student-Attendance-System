import React, { createContext, useState, useContext } from 'react';
import apiClient from '../services/api';


// Create StudentContext
const StudentContext = createContext();

// Provider component
export const StudentProvider = ({ children }) => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch students
  const fetchStudents = async () => {
    try {
      const response = await apiClient.get('/api/students')
      const students  = response.data.students
      console.log(students);

      setStudents(students);
    } catch (err) {
      setError('Failed to fetch students.');
    } finally {
      setLoading(false);
    }
  };

  // Update student
  const updateStudent = async (id, updatedData) => {
    try {
      // to implement api call later
      await apiClient.put(`/api/students/${id}`, updatedData);
      setStudents((prev) =>
        prev.map((student) => (student.id === id ? { ...student, ...updatedData } : student))
      );
    } catch (err) {
      setError('Failed to update student.');
    }
  };

  const deleteStudent = async (id) => {
    try {
      // to implement api call later
      await apiClient.delete(`/api/students/${id}`);
      const updatedStudents = students.filter((s) => s.id !== id);
      setStudents(updatedStudents);
    } catch (err) {
      setError('Failed to update student.');
    }
  }

  return (
    <StudentContext.Provider value={{ students, loading, error, fetchStudents, updateStudent, deleteStudent }}>
      {children}
    </StudentContext.Provider>
  );
};

// Custom hook to use context
export const useStudents = () => useContext(StudentContext);
