import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../../styles/IntroSection.css';

const IntroSection = () => {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setAnimate(true);
  }, []);

  return (
    <div className={`intro-section ${animate ? 'fade-in' : ''}`}>
      <div className="intro-header">
        <h2>Empowering Education with Seamless Attendance Tracking</h2>
        <p className="subheading">Revolutionizing how schools manage student attendance and engagement</p>
      </div>

      <div className="intro-content">
        <p>
          Welcome to the future of attendance management! Our Student Attendance System is more than just a tool; it's a comprehensive solution
          designed to enhance educational environments. By providing real-time insights into student attendance and engagement, we empower
          educators to make informed decisions and create more supportive learning environments.
        </p>

        <p>
          Our system offers a user-friendly interface that simplifies attendance tracking, generates detailed reports, and ensures data accuracy.
          Whether you're a teacher, administrator, or parent, our system provides the tools you need to stay connected and informed.
        </p>

        <ul>
          <li><strong>Real-Time Attendance Tracking:</strong> Monitor student presence instantly.</li>
          <li><strong>Comprehensive Reporting:</strong> Access detailed reports for data-driven decision-making.</li>
          <li><strong>Cross-Device Compatibility:</strong> Use our system on any device, anytime, anywhere.</li>
          <li><strong>User-Friendly Interface:</strong> Enjoy a simple and intuitive experience.</li>
          <li><strong>Enhanced Communication:</strong> Improve communication between teachers, parents, and administrators.</li>
        </ul>
      </div>

      <div className="intro-footer">
        <Link to="/create-account" className="cta-button">
          Start Your Journey
        </Link>
      </div>
    </div>
  );
};

export default IntroSection;
// import { Link } from 'react-router-dom';
// import '../../styles/IntroSection.css'; 

// const IntroSection = () => {
//     return (
//       <div className="intro-section">
//         <div className="intro-header">
//           <h2>Welcome to the Student Attendance System</h2>
//           <p className="subheading">Your all-in-one tool to monitor student attendance and activities</p>
//         </div>
        
//         <div className="intro-content">
//           <p>
//             Our Student Attendance System is designed to help teachers and administrators manage student attendance easily. With a real-time dashboard, 
//             you can track student presence, monitor activity, and access detailed attendance reports at your fingertips. 
//             Join now and streamline your school attendance process.
//           </p>
  
//           <ul>
//             <li>Real-time tracking of student attendance</li>
//             <li>Detailed reports for administrators and teachers</li>
//             <li>Accessible on any device</li>
//             <li>Simple and user-friendly interface</li>
//           </ul>
//         </div>
  
//         <div className="intro-footer">
//           <Link to="/register" className="cta-button">Get Started</Link>
//         </div>
//       </div>
//     );
//   };

// export default IntroSection;