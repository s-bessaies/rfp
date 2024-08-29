import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './form.css';

function Login({ onLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      // Retrieve the CSRF token from the cookies
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

      const response = await axios.post('/company/api/login/', formData, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,  // Add the CSRF token to the request headers
        }
      });

      console.log('Response:', response.data);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('username', formData.username);
      setSuccess(true);
      onLogin();
      navigate('/');
    } catch (error) {
      console.error('Error logging in:', error.response ? error.response.data : error.message);
      setError('Invalid username or password.');
    }
  };

  const handleSubscribe = () => {
    navigate('/form');
  };

  return (
    <div className="form-container">
      <h2>Login</h2>
      {success && <div className="success-message">Logged in successfully!</div>}
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="button-container">
          <button type="submit" className="subscribe">Login</button>
          <button type="button" onClick={handleSubscribe} className="comeback">Subscribe</button>
        </div>
      </form>
    </div>
  );
}

export default Login;
