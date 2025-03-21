import React, { useState } from "react";
import { useStudents } from "../../contexts/StudentContext";
import "../../styles/Modal.css";

const DeleteStudentModal = ({ student, onClose }) => {
  const { deleteStudent } = useStudents();
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (!student) return;

    setIsDeleting(true);

    try {
      console.log("Student log from handleDelete: ", student);
      
      await deleteStudent(student.student_id); // Simulated backend deletion
      onClose(); // Close the modal after deletion
    } catch (error) {
      console.error("Failed to delete student:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  if (!student) return null; // Do not render if no student is selected

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose} aria-label="Close">
          &times;
        </button>
        <h3 style={{ marginBottom: "1rem" }}>Delete Student</h3>
        <p style={{ marginBottom: "1rem" }}>
          Are you sure you want to delete <strong>{student.name}</strong>?
        </p>
        <div className="modal-actions">
          <button
            className="delete-button"
            onClick={handleDelete}
            disabled={isDeleting}
          >
            {isDeleting ? "Deleting..." : "Delete"}
          </button>
          <button className="cancel-button" onClick={onClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteStudentModal;
