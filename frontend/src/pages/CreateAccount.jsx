// src/pages/Login.js
import React, { use, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { auth } from '../config/firebase';
import { createUserWithEmailAndPassword, signInWithPopup,GoogleAuthProvider} from 'firebase/auth'
import '../styles/Auth.css'; // Auth.css file is asyled for the login and create account pages
import {saveGoogleUserToCookie, getUserIdFromCookie} from '../services/auth.service';

const CreateAccount = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const result = await createUserWithEmailAndPassword(auth, email, password);
      const user = result.user;
      saveGoogleUserToCookie(user)
      navigate('/'); // Redirect to dashboard after successful login
    } catch (error) {
      setError(error.message);
    }
  };

  const handleGoogleLogin = async () => {
    const provider = new GoogleAuthProvider();

    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;
      saveGoogleUserToCookie(user)
      navigate('/'); // Redirect after successful login
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2 className='login-head'>Sign up</h2>
        {error && <div className="error-message">{error}</div>}
        <input
          className='login-input'
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className='login-input'
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button className='login-button' type="submit">Sign up</button>
      </form>

      <div className="google-auth">
        <button onClick={handleGoogleLogin} className="google-btn">
          Sign up with Google
        </button>
      </div>
      <span className='alt-auth-statement'>Already have an account?
        <Link to='/login'>Login account</Link>
        </span>
    </div>
  );
};

export default CreateAccount;
