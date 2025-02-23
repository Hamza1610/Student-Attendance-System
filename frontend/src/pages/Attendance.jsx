import '../styles/Attendance.css';
import AttendanceTable from '../components/attendance/AttendanceTable';
import { AttendanceProvider } from '../contexts/AttendanceContext';

const AttendanceTracking = () => {

  return (
    <div className='attendance'>
      <AttendanceProvider>
        <AttendanceTable />
      </AttendanceProvider>
    </div>
  )
}
export default AttendanceTracking;
