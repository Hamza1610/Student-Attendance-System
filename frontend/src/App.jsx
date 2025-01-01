// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AuthProvider from './contexts/AuthContext';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Layout from './components/layout/Layout';
import PrivateRoute from './components/auth/PrivateRoute';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import StudentRegistration from './pages/StudentRegistration';
import AttendanceTracking from './pages/Attendance';
import AttendanceRecords from './pages/AttendanceRecords';
import StudentDetails from './pages/StudentDetails';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';
import Profile from './pages/Profile';
import CreateAccount from './pages/CreateAccount';
import IntroSection from './components/dashboard/IntroSection';

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <ToastContainer position="top-right" autoClose={3000} />
        <Routes>
          {/* Login route */}
          <Route path="/login" element={<Login />} />
          {/* Create account route */}
          <Route path="/create-account" element={<CreateAccount />} />
        
          {/* Home route */}
          <Route path="/" element={
            <Layout>
              <IntroSection />
              <PrivateRoute>
                  <Dashboard />
              </PrivateRoute>
            </Layout>
            }
          />
  
          {/* Attendance related */}
          <Route
            path="/attendance"
            element={
              <Layout>
                <PrivateRoute>
                  <AttendanceTracking />
                </PrivateRoute>
              </Layout>
            }
          />

          <Route
            path="/attendance/records"
            element={
              <Layout>
                <PrivateRoute>
                  <AttendanceRecords />
                </PrivateRoute>
              </Layout>
            }
          />

          {/* Student registration route and related*/}
          <Route
            path="/students/register"
            element={
              <Layout>
                <PrivateRoute>
                  <StudentRegistration />
                </PrivateRoute>
              </Layout>
            }
          />

         `<Route
            path="/students/:id"
            element={
              <Layout>
                <PrivateRoute>
                  <StudentDetails />
                </PrivateRoute>
              </Layout>
            }
          />
          
          {/* Settings */}
          <Route
            path="/profile"
            element={
              <Layout>
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
              </Layout>
            }
          />

          {/* Settings */}
          <Route
            path="/settings"
            element={
              <Layout>
                <PrivateRoute>
                  <Settings />
                </PrivateRoute>
              </Layout>
            }
          />
          {/* Not found */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;