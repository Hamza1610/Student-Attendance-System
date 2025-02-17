// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuthProvider from './contexts/AuthContext';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Layout from './components/layout/Layout';
import PrivateRoute from './components/auth/PrivateRoute';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AttendanceTracking from './pages/Attendance';
import NotFound from './pages/NotFound';
import Profile from './pages/Profile';
import CreateAccount from './pages/CreateAccount';
import Students from './pages/Students';

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
          <Route path="/" element={<Dashboard />}
          />
  
          {/* Attendance related */}
          <Route
            path="/attendance"
            element={
              <Layout>
                <PrivateRoute>
                  <AttendanceTracking />
                </PrivateRoute>
                {/* <AttendanceTracking /> */}
              </Layout>
            }
          />
          
          {/* Profile */}
          <Route
            path="/profile"
            element={
              <Layout>
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
                {/* <Profile /> */}
              </Layout>
            }
          />

          {/* Students */}
          <Route
            path="/students"
            element={
              <Layout>
                <PrivateRoute>
                  <Students />
                </PrivateRoute>
                {/* <Students /> */}
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