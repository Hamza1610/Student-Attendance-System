import React, { useState, useEffect } from 'react';
import { useStudents } from '../../contexts/StudentContext';
import apiClient from '../../services/api';
import '../../styles/Modal.css'; // Import shared modal styles

const EditStudentModal = ({ student, onClose }) => {
  const { fetchStudents } = useStudents();
  const [formData, setFormData] = useState({
    name: '',
    student_id: '',
    email: '',
    class_name: '',
    registered_by: '',
  });
  const [faceEmbedding, setFaceEmbedding] = useState(null); // Handle image separately
  const [error, setError] = useState(null);

  useEffect(() => {
    if (student) {
      setFormData({
        name: student.name,
        student_id: student.student_id,
        email: student.email,
        class_name: student.class_name,
        registered_by: student.registered_by,
      });
    }
  }, [student]);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setFaceEmbedding(file);
  };

  const handleSubmit = async () => {
    if (!student) return;

    try {
      const formDataPayload = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        formDataPayload.append(key, value);
      });

      if (faceEmbedding) {
        formDataPayload.append('face_embedding', faceEmbedding);
      }

      await apiClient.put(`/api/students/${student.id}`, formDataPayload, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      await fetchStudents(); // Refresh the list of students
      onClose(); // Close the modal
    } catch (err) {
      setError('Failed to update student. Please try again.');
    }
  };

  if (!student) return null; // Do not render if no student is selected

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Edit Student</h3>
        {error && <div className="error-message">{error}</div>}
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            id="name"
            type="text"
            placeholder="Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label htmlFor="student_id">Student ID</label>
          <input
            id="student_id"
            type="text"
            placeholder="Student ID"
            value={formData.student_id}
            onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label htmlFor="class_name">Class</label>
          <input
            id="class_name"
            type="text"
            placeholder="Class"
            value={formData.class_name}
            onChange={(e) => setFormData({ ...formData, class_name: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label htmlFor="face_embedding">Face Embedding</label>
          <input
            id="face_embedding"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>
        <div className="form-group">
          <label htmlFor="registered_by">Registered By</label>
          <input
            id="registered_by"
            type="text"
            placeholder="Registered By"
            value={formData.registered_by}
            onChange={(e) => setFormData({ ...formData, registered_by: e.target.value })}
          />
        </div>
        <div className="modal-actions">
          <button className="btn-save" onClick={handleSubmit}>
            Save
          </button>
          <button className="btn-cancel" onClick={onClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditStudentModal;
