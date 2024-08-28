import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Form from './Form';
import Home from './home';
import Login from './login';
import PDFUpload from './analyze-rfp';
import UpdateInformation from './update_form'; 
import RFPHistory from './RFPHistory'; // Import the new component
import WelcomePage from './WelcomePage';
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={
            isAuthenticated ? (
              <Navigate to="/" />
            ) : (
              <Login onLogin={() => setIsAuthenticated(true)} />
            )
          }
        />
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Home onLogout={() => setIsAuthenticated(false)} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/update"
          element={
            isAuthenticated ? (
              <UpdateInformation />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/form"
          element={<Form />}
        />
        <Route
          path="/analyze-rfp"
          element={
            isAuthenticated ? (
              <PDFUpload />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/rfp-history"
          element={
            isAuthenticated ? (
              <RFPHistory />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/welcome"
          element={<WelcomePage />} // Set the WelcomePage as the default route
        />
      </Routes>
    </Router>
  );
}

export default App;
