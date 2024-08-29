import React from 'react';
import './Navbar.css'; // Ensure this CSS file contains the styles
import {  useNavigate } from 'react-router-dom';

const Navbar = ({ onLogout }) => {
    const navigate = useNavigate();
    const handleUpdateInformation = () => {
        navigate('/update'); 
      };
      const handleViewHistory = () => {
        navigate('/rfp-history'); 
      };
  const handlelogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    onLogout();
    navigate('/login');  
  };
    return (
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-logo">
            <a href="#head">RFP Analyzer</a>
          </div>
          <ul className="navbar-links">
            <li><a onClick={handleUpdateInformation} >Update Information</a></li>
            <li><a onClick={handleViewHistory}>My Activity</a></li>
            <li><a onClick={handleViewHistory}>Contact Us</a></li>
          </ul>
          <div className="navbar-auth">
            <a onClick={handlelogout} className="auth-button">Logout</a>
          </div>
        </div>
      </nav>
    );
  };
  

export default Navbar;
