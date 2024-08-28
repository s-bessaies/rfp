import React from 'react';
import './Navbar.css'; 

const Navbar = () => {
    return (
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-logo">
            <a href="#head">RFP Analyzer</a>
          </div>
          <ul className="navbar-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="#head">Home</a></li>
          </ul>
          <div className="navbar-auth">
            <a href="/login" className="auth-button">Login</a>
            <a href="/form" className="auth-button">Sign Up</a>
          </div>
        </div>
      </nav>
    );
  };
  

export default Navbar;
