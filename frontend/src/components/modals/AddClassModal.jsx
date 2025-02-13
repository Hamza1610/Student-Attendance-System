import React, { useState } from 'react';
import './../../styles/Modal.css';
import apiClient from '../../services/api';
import { getUserIdFromCookie } from '../../services/auth.service';

const AddClassModal = ({ isOpen, onClose }) => {
  const [newClass, setNewClass] = useState({
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    status: 'active',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewClass((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Build form data using the FastAPI required fields.
    const formData = new FormData();
    formData.append('name', newClass.name);
    formData.append('description', newClass.description);
    formData.append('start_date', newClass.start_date);
    formData.append('end_date', newClass.end_date);
    formData.append('status', newClass.status);
    formData.append('teacher_id', getUserIdFromCookie());

    try {
      await apiClient.post('/api/classes', formData);
      // Optionally, refresh any class list here if needed.
      setNewClass({
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        status: 'active',
      });
      onClose(); // Close the modal on success.
    } catch (err) {
      console.error(err);
      setError('Failed to create class. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>&times;</button>
        <form onSubmit={handleSubmit}>
          <h3>Add New Class</h3>
          {error && <p className="error">{error}</p>}
          <input
            type="text"
            name="name"
            placeholder="Class Name"
            value={newClass.name}
            onChange={handleInputChange}
            required
          />
          <textarea
            name="description"
            placeholder="Description"
            value={newClass.description}
            onChange={handleInputChange}
            required
          />
          <input
            type="date"
            name="start_date"
            placeholder="Start Date (YYYY-MM-DD)"
            value={newClass.start_date}
            onChange={handleInputChange}
            required
          />
          <input
            type="date"
            name="end_date"
            placeholder="End Date (YYYY-MM-DD)"
            value={newClass.end_date}
            onChange={handleInputChange}
            required
          />
          <select
            name="status"
            value={newClass.status}
            onChange={handleInputChange}
            required
          >
            <option value="active">Active</option>
            <option value="closed">Closed</option>
          </select>
          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Class'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddClassModal;
