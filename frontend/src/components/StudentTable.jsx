import React, { useEffect, useState } from 'react';
import { useStudents } from '../contexts/StudentContext';
import { getAuth, onAuthStateChanged } from 'firebase/auth';

import { FaEye, FaEdit, FaUsersSlash } from 'react-icons/fa';
import '../styles/StudentsTable.css';
import AddStudentModal from './modals/AddStudentModal';
import EditStudentModal from './modals/EditStudentModal';
import ViewStudentModal from './modals/ViewStudentModal';
import DeleteStudentModal from './modals/DeleteStudentModal';
import app from '../config/firebase';

const StudentTable = () => {
  const { students, loading, error, fetchStudents } = useStudents();
  const [currentUser, setCurrentUser] = useState(null);
  const [viewStudent, setViewStudent] = useState(null);
  const [editStudent, setEditStudent] = useState(null);
  const [deleteStudent, setDeleteStudent] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // Monitor auth state
  useEffect(() => {
    const auth = getAuth(app);
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setCurrentUser(user);
        fetchStudents(user.uid);
      }
    });
    return () => unsubscribe();
  }, []);

  return (
    <div className="student-list">
      {loading && <div>Loading...</div>}
      {error && <div className="error">{error}</div>}
      
      <button className='add-student-btn' onClick={() => setIsModalOpen(true)}>Add Student</button>
      <AddStudentModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />

      <table className="students-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Class</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {students && students.map((student) => (
            <tr key={student.id}>
              <td>{student.name}</td>
              <td>{student.class_name}</td>
              <td className='table-actions'>
                <button onClick={() => setEditStudent(student)}>
                  Edit <FaEdit size={20} className="icon" />
                </button>
                <button onClick={() => setViewStudent(student)}>
                  View <FaEye size={20} className="icon" />
                </button>
                <button onClick={() => setDeleteStudent(student)}>
                  Delete <FaUsersSlash size={20} className="icon" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <EditStudentModal student={editStudent} onClose={() => setEditStudent(null)} />
      <ViewStudentModal student={viewStudent} onClose={() => setViewStudent(null)} />
      <DeleteStudentModal student={deleteStudent} onClose={() => setDeleteStudent(null)} />
    </div>
  );
};

export default StudentTable;
