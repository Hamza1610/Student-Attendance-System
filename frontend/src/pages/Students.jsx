import React from 'react';
import StudentTable from '../components/StudentTable';
import { StudentProvider } from '../contexts/StudentContext';

const Students = () => {
  return (
  
  
    <div className='settings'>
        <StudentProvider>
          <StudentTable />
        </StudentProvider>
    </div>


    
    

  )
};

export default Students;
