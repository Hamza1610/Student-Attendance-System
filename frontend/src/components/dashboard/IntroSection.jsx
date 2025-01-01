import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/IntroSection.css'; 

const IntroSection = () => {
    return (
      <div className="intro-section">
        <div className="intro-header">
          <h2>Welcome to the Student Attendance System</h2>
          <p className="subheading">Your all-in-one tool to monitor student attendance and activities</p>
        </div>
        
        <div className="intro-content">
          <p>
            Our Student Attendance System is designed to help teachers and administrators manage student attendance easily. With a real-time dashboard, 
            you can track student presence, monitor activity, and access detailed attendance reports at your fingertips. 
            Join now and streamline your school attendance process.
          </p>
  
          <ul>
            <li>Real-time tracking of student attendance</li>
            <li>Detailed reports for administrators and teachers</li>
            <li>Accessible on any device</li>
            <li>Simple and user-friendly interface</li>
          </ul>
        </div>
  
        <div className="intro-footer">
          <Link to="/register" className="cta-button">Get Started</Link>
        </div>
      </div>
    );
  };

export default IntroSection;