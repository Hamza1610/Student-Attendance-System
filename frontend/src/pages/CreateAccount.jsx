// src/pages/Login.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { auth } from '../config/firebase';
import { createUserWithEmailAndPassword, signInWithPopup,GoogleAuthProvider} from 'firebase/auth'
import '../styles/Auth.css'; // Auth.css file is asyled for the login and create account pages

const CreateAccount = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createUserWithEmailAndPassword(auth, email, password);
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
      console.log('Google User ID:', user.uid); // You can use this to verify the user from your backend
      navigate('/'); // Redirect after successful login
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2 className='login-head'>Login</h2>
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
        <button className='login-button' type="submit">Login</button>
      </form>

      <div className="google-auth">
        <button onClick={handleGoogleLogin} className="google-btn">
          Sign in with Google
        </button>
      </div>
      <span className='alt-auth-statement'>Already have an account?
        <Link to='/login'>Login account</Link>
        </span>
    </div>
  );
};

export default CreateAccount;
