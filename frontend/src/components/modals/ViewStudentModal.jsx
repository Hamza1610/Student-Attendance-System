import React from 'react';
import '../../styles/Modal.css';

const ViewStudentModal = ({ student, onClose }) => {
  if (!student) return null; // Do not render if no student is selected


  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <h3 style={{ marginBottom: '1rem' }}>View Student Details</h3>
        <p style={{ marginBottom: '1rem' }}>
          <strong>Name:</strong> {student.name}
        </p>
        <p style={{ marginBottom: '1rem' }}>
          <strong>Student ID:</strong> {student.student_id}
        </p>
        <p style={{ marginBottom: '1rem' }}>
          <strong>Email:</strong> {student.email}
        </p>
        <p style={{ marginBottom: '1rem' }}>
          <strong>Class:</strong> {student.class_name}
        </p>
        <div className="modal-actions">
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};

export default ViewStudentModal;
