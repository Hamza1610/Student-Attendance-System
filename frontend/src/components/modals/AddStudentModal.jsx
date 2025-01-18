import React, { useState } from 'react';
import { useStudents } from '../../contexts/StudentContext';
import './../../styles/Modal.css'
import apiClient from '../../services/api';
import { getUserIdFromCookie } from '../../services/auth.service';

const AddStudentModal = ({ isOpen, onClose }) => {
  const { fetchStudents } = useStudents();
  const [newStudent, setNewStudent] = useState({
    name: '',
    student_id: '',
    email: '',
    class_name: '',
    image: null,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewStudent((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    setNewStudent((prev) => ({ ...prev, image: e.target.files[0] }));
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('name', newStudent.name);
    formData.append('student_id', newStudent.student_id);
    formData.append('email', newStudent.email);
    formData.append('class_name', newStudent.class_name);
    formData.append('user_id', getUserIdFromCookie())
    if (newStudent.image) {
      formData.append('image', newStudent.image);
    }
    // formData.append('user_id', 'CURRENT_USER_UID'); // Replace with actual Firebase UID

    try {
      await apiClient.post('/api/students/register', formData);
      await fetchStudents();
      setNewStudent({ name: '', student_id: '', email: '', class_name: '', image: null });
      onClose(); // Close modal on success
    } catch (err) {
      setError('Failed to add student. Please try again.');
      console.log(err);
      
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <form onSubmit={handleAddStudent}>
          <h3>Add New Student</h3>
          {error && <p className="error">{error}</p>}
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={newStudent.name}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="student_id"
            placeholder="Student ID"
            value={newStudent.student_id}
            onChange={handleInputChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={newStudent.email}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="class_name"
            placeholder="Class ID"
            value={newStudent.class_name}
            onChange={handleInputChange}
            required
          />
          <input type="file" name="image" onChange={handleFileChange} />
          <button type="submit" disabled={loading}>
            {loading ? 'Adding...' : 'Add Student'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddStudentModal;
