import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Profile.css'; // Importing the CSS file for styles
import { getUserIdFromCookie } from '../services/auth.service';
import apiClient from '../services/api';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);
  const userId = getUserIdFromCookie();
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        console.log("UserId:", userId);
        
        if (!userId) {
          setError("You are not authorized to vied this page please go back and login")
        }
        const response = await apiClient.get(`/api/profile/${userId}`);
        setProfile(response.data);
      } catch (err) {
        setError(err.response ? err.response.data.detail : 'An error occurred');
      }
    };

    fetchProfile();
  }, [userId]);

  if (error) {
    return (
      <div className="profile-container error">
        <h1>Error</h1>
        <p className="error-message">{error}</p>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="profile-container loading">
        <h1>Loading...</h1>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <img className="profile-image" src={profile.photo_url} alt={`${profile.name}'s Profile`} />
        <h1 className="profile-name">{profile.name}</h1>
        <p className="profile-email"><strong>Email:</strong> {profile.email}</p>
        <p className="profile-role"><strong>Role:</strong> {profile.role}</p>
      </div>
    </div>
  );
};

export default Profile;
