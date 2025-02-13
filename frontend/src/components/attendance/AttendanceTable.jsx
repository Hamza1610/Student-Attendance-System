import React, { useEffect, useState } from 'react';
import{ useAttendance } from '../../contexts/AttendanceContext';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { FaEdit } from 'react-icons/fa';
import '../../styles/AttendanceTable.css';
import app from '../../config/firebase';
import { saveGoogleUserToCookie } from '../../services/auth.service';
import AddClassModal from '../modals/AddClassModal';

const AttendanceTable = () => {

  // const [isModalOpen, setIsModalOpen] = useState(false);
  const { fetchClasses, updateStudentAttendance, classes, loading, error } = useAttendance();
  const [currentUser, setCurrentUser] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleCreateClass = () => {
    setIsModalOpen(true);
  }
  // Monitor auth state
  useEffect(() => {
    const auth = getAuth(app);
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setCurrentUser(user);
        saveGoogleUserToCookie(user);
        fetchClasses()
      }
    });
    return () => unsubscribe();
  }, []);


  return (
    <div className="student-list">
      {loading && <div>Loading...</div>}
      {error && <div className="error">{error}</div>}

      <button className='add-class-btn' onClick={handleCreateClass}>Create class</button>
      {/a* Modal */}
      <AddClassModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
      <table className="students-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {classes && classes.map((classDetail) => (
            <tr key={classDetail.name}>
              <td>{classDetail.name}</td>
              <td>{classDetail.description}</td>
              <td className='table-actions'>
                <button>
                  Take attendance <FaEdit size={20} className="icon" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AttendanceTable;