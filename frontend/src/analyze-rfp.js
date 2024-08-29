import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './analyze.css'
const PDFUpload = () => {
  const [historyData, setData] = useState([]);
  const [selectedRFP, setSelectedRFP] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  useEffect(() => {
    fetch(`/process-pdf/api/rfp-history/?username=${username}`)
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          console.log(data.message);
        } else {
          setData(data);
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, [username]);

  const handleRFPClick = (rfp) => {
    setSelectedRFP(rfp);
    setPdfFile(null);
  };

  const handleReturnHome = () => {
    navigate('/');
  };

  const handleFileUpload = (event) => {
    setPdfFile(event.target.files[0]);
  };

  const handleAnalyzeRFP = () => {
    if (!pdfFile) {
      setMessage('Please upload a PDF first.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('pdf', pdfFile);
    formData.append('username', username);

    axios.put(`/process-pdf/api/extract_attributes/?username=${username}`, formData)
      .then(response => {
        setMessage('RFP analysis successful!');
        setSelectedRFP(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("There was an error analyzing the RFP!", error);
        setMessage('Failed to analyze the RFP.');
        setLoading(false);
      });
  };

  const handleAnalyzeNewRFP = () => {
    setSelectedRFP(null);
    setPdfFile(null);
    setMessage('');
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const renderCell = (value) => {
    if (
        (Array.isArray(value) && value.length === 0) ||
        value === 'null' ||
        value === undefined ||
        value === null ||
        (typeof value === 'string' && value.trim() === '')
    ) {
        return null;
    }
    return value;
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', margin: 0, padding: 0 }}>
      {/* Sidebar */}
      <div
        style={{
          width: sidebarOpen ? '280px' : '80px',
          backgroundColor: '#1b1b1b',
          color: '#ffffff',
          padding: '20px',
          height: '100vh',
          position: 'fixed',
          top: 0,
          left: 0,
          marginRight:30,
          borderRadius: '0 16px 16px 0',
          overflowY: 'auto',
          transition: 'width 0.3s ease',
          boxShadow: '2px 0 12px rgba(0, 0, 0, 0.5)',
          zIndex: 1000,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          {sidebarOpen && (
            <h4 style={{ fontWeight: 'bold', textAlign: 'center', flexGrow: 1 }}>
              RFP History
            </h4>
          )}
          <button onClick={toggleSidebar} style={{ backgroundColor: 'transparent', border: 'none', color: '#ffffff' }}>
            {sidebarOpen ? '⬅' : '➡'}
          </button>
        </div>

        {sidebarOpen && (
          <>
            <ul style={{ padding: 0, listStyleType: 'none', marginBottom: '20px' }}>
              {historyData.map((rfp, index) => (
                <React.Fragment key={index}>
                  <li
                    onClick={() => handleRFPClick(rfp)}
                    style={{
                      borderRadius: '8px',
                      padding: '12px',
                      cursor: 'pointer',
                      backgroundColor: selectedRFP === rfp ? '#ff6f61' : '#2b2b2b',
                      marginBottom: '10px',
                      color: '#ffffff',
                      textAlign: 'center',
                      transition: 'background-color 0.3s ease',
                    }}
                  >
                    {rfp.pdf_name}
                  </li>
                  {index < historyData.length - 1 && <hr style={{ backgroundColor: '#4a4a4a', border: 'none', height: '1px' }} />}
                </React.Fragment>
              ))}
            </ul>

            <button
              onClick={handleAnalyzeNewRFP}
              style={{
                backgroundColor: '#ff6f61',
                color: '#ffffff',
                fontWeight: 'bold',
                borderRadius: '8px',
                border: 'none',
                padding: '12px',
                width: '100%',
                cursor: 'pointer',
                transition: 'background-color 0.3s ease',
              }}
            >
              New Chat
            </button>
          </>
        )}
      </div>

      {/* Main Content Area */}
      <div
        style={{
          
          marginLeft: sidebarOpen ? '300px' : '100px',
          padding: '40px',
          backgroundColor: '#2e2e2e',
          color: '#ffffff',
          minHeight: '100vh',
          transition: 'margin-left 0.3s ease',
          borderRadius: '16px',
          width: '100%',
        }}
      >
        <div style={{ padding: '24px', width: '70%', borderRadius: '16px', backgroundColor: '#3c3c3c', color: '#ffffff', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)', margin: '0 auto' }}>

          <h2 style={{ fontWeight: 'bold', marginBottom: '24px', textAlign: 'center', fontSize: '1.8em' }}>
            {selectedRFP ? selectedRFP.pdf_name : 'Upload and Analyze RFP'}
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '20px', marginBottom: '24px' }}>
            <button
              onClick={handleReturnHome}
              style={{
                backgroundColor: '#ff6f61',
                color: '#ffffff',
                fontWeight: 'bold',
                borderRadius: '8px',
                border: 'none',
                padding: '14px',
                width: '100%',
                cursor: 'pointer',
                transition: 'background-color 0.3s ease',
              }}
            >
              Return to Home
            </button>

            {selectedRFP && (
              <button
                onClick={handleAnalyzeNewRFP}
                style={{
                  backgroundColor: '#ff6f61',
                  color: '#ffffff',
                  fontWeight: 'bold',
                  borderRadius: '8px',
                  border: 'none',
                  padding: '14px',
                  width: '100%',
                  cursor: 'pointer',
                  transition: 'background-color 0.3s ease',
                }}
              >
                Analyze New RFP
              </button>
            )}

            {!selectedRFP && (
              <input
                type="file"
                onChange={handleFileUpload}
                accept="application/pdf"
                style={{
                  padding: '14px',
                  backgroundColor: '#424242',
                  color: '#ffffff',
                  border: '1px solid #ff6f61',
                  borderRadius: '8px',
                  width: '100%',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s ease',
                }}
              />
            )}

            <button
              onClick={handleAnalyzeRFP}
              disabled={!pdfFile}
              style={{
                backgroundColor: pdfFile ? '#ff6f61' : '#9e9e9e',
                color: '#ffffff',
                fontWeight: 'bold',
                borderRadius: '8px',
                border: 'none',
                padding: '14px',
                width: '100%',
                cursor: pdfFile ? 'pointer' : 'not-allowed',
                transition: 'background-color 0.3s ease',
              }}
            >
              Analyze RFP
            </button>
          </div>

          {selectedRFP && (
            <div style={{ marginTop: '20px' }}>
              <h2 style={{ marginBottom: '16px', fontSize: '1.6em' }}>{renderCell(selectedRFP?.pdf_name)}</h2>
              {renderCell(selectedRFP?.sector) && <p><strong>Sector:</strong> {renderCell(selectedRFP?.sector)}</p>}
              {renderCell(selectedRFP?.dates) && <p><strong>Dates:</strong> {renderCell(selectedRFP?.dates)}</p>}
              {renderCell(selectedRFP?.location) && <p><strong>Location:</strong> {renderCell(selectedRFP?.location)}</p>}
              {renderCell(selectedRFP?.minimum_experience) && <p><strong>Minimum Experience:</strong> {renderCell(selectedRFP?.minimum_experience)}</p>}
              {renderCell(selectedRFP?.required_certifications) && <p><strong>Required Certifications:</strong> {renderCell(selectedRFP?.required_certifications)}</p>}
              {renderCell(selectedRFP?.similar_project_references) && <p><strong>Similar Project References:</strong> {renderCell(selectedRFP?.similar_project_references)}</p>}
              {renderCell(selectedRFP?.it_infrastructure) && <p><strong>IT Infrastructure:</strong> {renderCell(selectedRFP?.it_infrastructure)}</p>}
              {renderCell(selectedRFP?.network_infrastructure) && <p><strong>Network Infrastructure:</strong> {renderCell(selectedRFP?.network_infrastructure)}</p>}
              {renderCell(selectedRFP?.virtualization) && <p><strong>Virtualization:</strong> {renderCell(selectedRFP?.virtualization)}</p>}
              {renderCell(selectedRFP?.programming_languages) && <p><strong>Programming Languages:</strong> {renderCell(selectedRFP?.programming_languages)}</p>}
              {renderCell(selectedRFP?.cloud_computing_data_management_ai_skills) && <p><strong>Cloud, Data & AI Skills:</strong> {renderCell(selectedRFP?.cloud_computing_data_management_ai_skills)}</p>}
              {renderCell(selectedRFP?.cybersecurity_devops_big_data_skills) && <p><strong>Cybersecurity, DevOps & Big Data Skills:</strong> {renderCell(selectedRFP?.cybersecurity_devops_big_data_skills)}</p>}
              {renderCell(selectedRFP?.iot_network_telecom_blockchain_skills) && <p><strong>IoT, Network & Blockchain Skills:</strong> {renderCell(selectedRFP?.iot_network_telecom_blockchain_skills)}</p>}
              {renderCell(selectedRFP?.automation_orchestration_data_analysis_skills) && <p><strong>Automation, Orchestration & Data Analysis Skills:</strong> {renderCell(selectedRFP?.automation_orchestration_data_analysis_skills)}</p>}
              {renderCell(selectedRFP?.technical_support_and_maintenance) && <p><strong>Technical Support & Maintenance:</strong> {renderCell(selectedRFP?.technical_support_and_maintenance)}</p>}
              {renderCell(selectedRFP?.reliability) && <p><strong>Reliability:</strong> {renderCell(selectedRFP?.reliability)}</p>}
              {renderCell(selectedRFP?.flexibility) && <p><strong>Flexibility:</strong> {renderCell(selectedRFP?.flexibility)}</p>}
              {renderCell(selectedRFP?.integrity) && <p><strong>Integrity:</strong> {renderCell(selectedRFP?.integrity)}</p>}
              {renderCell(selectedRFP?.availability) && <p><strong>Availability:</strong> {renderCell(selectedRFP?.availability)}</p>}
              {renderCell(selectedRFP?.solution_scalability) && <p><strong>Solution Scalability:</strong> {renderCell(selectedRFP?.solution_scalability)}</p>}
              {renderCell(selectedRFP?.project_management_approaches) && <p><strong>Project Management Approaches:</strong> {renderCell(selectedRFP?.project_management_approaches)}</p>}
              {renderCell(selectedRFP?.project_resources) && <p><strong>Project Resources:</strong> {renderCell(selectedRFP?.project_resources)}</p>}
              {renderCell(selectedRFP?.training) && <p><strong>Training:</strong> {renderCell(selectedRFP?.training)}</p>}
              {renderCell(selectedRFP?.deployment) && <p><strong>Deployment:</strong> {renderCell(selectedRFP?.deployment)}</p>}
              {renderCell(selectedRFP?.legal_compliance) && <p><strong>Legal Compliance:</strong> {renderCell(selectedRFP?.legal_compliance)}</p>}
              {renderCell(selectedRFP?.regulations) && <p><strong>Regulations:</strong> {renderCell(selectedRFP?.regulations)}</p>}
              {renderCell(selectedRFP?.score) && <p><strong>Score:</strong> {renderCell(selectedRFP?.score)}%</p>}
            </div>
          )}

            {loading && (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              <div className="loading-spinner" style={{ marginRight: '10px' }} />
              <p>Analyzing RFP...</p>
            </div>
          )}
          {message && <p>{message}</p>}
        </div>
      </div>
    </div>
  );
};

export default PDFUpload;
