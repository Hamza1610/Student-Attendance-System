import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css';
import IntroSection from '../components/dashboard/IntroSection';
import apiClient from '../services/api';

const fetchDashboardData = async () => {
  const response = await apiClient.get("/api/students");
  const students = response.data.students;
  if (!students) {
    // Example data
    return {
      totalStudents: 120,
      presentStudents: 95,
      absentStudents: 25,
      recentActivity: {
        lastCheckedIn: "John Doe",
        time: "10:30 AM",
      }
    };
  }
  // Example data
  return students[-1]
};

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);

  // Fetch the dashboard data when the component mounts
  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchDashboardData();
      setDashboardData(data);
    };
    fetchData();
  }, []);

  return (
    <div className="dashboard" style={{ width: '100%', height: '100%', padding: '20px' }}>
      <h1>Dashboard</h1>
      
      {!dashboardData ? (
        <p>Loading dashboard...</p>
      ) : (
        <div className="dashboard-content">
          {/* Intro for unregistered users */}
          {/* <IntroSection /> */}

          {/* Dashboard metrics for registered users */}
          <div className="metrics" style={{ display: 'flex', justifyContent: 'space-around', marginTop: '20px' }}>
            <div className="metric-box">
              <h3>Total Students</h3>
              <p>{dashboardData.totalStudents}</p>
            </div>
            <div className="metric-box">
              <h3>Present Students</h3>
              <p>{dashboardData.presentStudents}</p>
            </div>
            <div className="metric-box">
              <h3>Absent Students</h3>
              <p>{dashboardData.absentStudents}</p>
            </div>
          </div>

          {/* Recent activity section */}
          <div className="recent-activity" style={{ marginTop: '40px' }}>
            <h3>Recent Activity</h3>
            <div className="activity-item" style={{ marginBottom: '10px' }}>
              <p><strong>Last Checked In:</strong> {dashboardData.recentActivity.lastCheckedIn}</p>
              <p><strong>Time:</strong> {dashboardData.recentActivity.time}</p>
            </div>
          </div>

          {/* Attendance Overview */}
          <div className="attendance-overview" style={{ marginTop: '40px' }}>
            <h3>Attendance Overview</h3>
            <p>This section will provide detailed stats on student attendance trends and patterns.</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
