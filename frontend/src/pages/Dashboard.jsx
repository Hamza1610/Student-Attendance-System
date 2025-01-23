import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css';
import IntroSection from '../components/dashboard/IntroSection';
import apiClient from '../services/api';
import Layout from '../components/layout/Layout';

const fetchDashboardData = async () => {
  try {
    const response = await apiClient.get("/api/students");
    const students = await response.data.students;

    if (students) {
      console.log('Array length', students.length);
      console.log('Array length', students[students.length - 1]);

      return {
        totalStudents: students.length,
        totalClass: 2,
        absentStudents: 25,
        recentActivity: {
          lastCheckedIn: students[students.length - 1].name,
          regNum: students[students.length - 1].student_id,
          className: students[students.length - 1].class_name
        }
      };  
    }
    
  
  } catch (error) {
    console.log("Erro msg:", error);
    
    return {
      totalStudents: 0,
      totalClass: 0,
      absentStudents: 0,
      recentActivity: {
        lastCheckedIn: "No activity",
        regNum: "No reg number",
        className: "No class name"
      }
    };
  }
};

export const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);

  // Fetch the dashboard data when the component mounts
  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchDashboardData();
      console.log("DashBoard data:", data);
      
      setDashboardData(data);
    };
    fetchData();
  }, []);

  return (
    <Layout>
      <div className="dashboard" style={{ width: '100%', height: '100%', padding: '20px' }}>
        <h1>Dashboard</h1>
        
        {!dashboardData ? (
          <p>Loading dashboard...</p>
        ) : (
          <div className="dashboard-content">
            {/* Intro for unregistered users */}
            <IntroSection />

            {/* Dashboard metrics for registered users */}
            <div className="metrics" style={{ display: 'flex', justifyContent: 'space-around', marginTop: '20px' }}>
              <div className="metric-box">
                <h3>Total Students</h3>
                <p>{dashboardData.totalStudents}</p>
              </div>

              <div className="metric-box">
                <h3>Total Class</h3>
                <p>{dashboardData.totalClass}</p>
              </div>
            </div>

            {/* Recent activity section */}
            <div className="recent-activity" style={{ marginTop: '40px' }}>
              <h3>Recent Activity</h3>
              <div className="activity-item" style={{ marginBottom: '10px' }}>
                <p><strong>Last Student Checked In:</strong> {dashboardData.recentActivity.lastCheckedIn}</p>
                <p><strong>Class:</strong> {dashboardData.recentActivity.className}</p>
                <p><strong>Reg number:</strong> {dashboardData.recentActivity.regNum}</p>
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
    </Layout>
  );
};

export default Dashboard;
