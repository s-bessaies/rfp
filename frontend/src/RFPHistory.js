import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RFPHistory.css'; 
import { useNavigate } from 'react-router-dom';

function RFPHistory() {
  const [historyData, setHistoryData] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [viewDetails, setViewDetails] = useState(false);
  const username = localStorage.getItem('username'); 
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`/process-pdf/api/rfp-history/?username=${username}`)
      .then(response => {
        setHistoryData(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching the RFP history!", error);
      });
  }, [username]);

  const handleRowClick = (item) => {
    setSelectedItem(item);
    setViewDetails(true);
  };

  const handleDashboardClick = () => {
    navigate('/');
  };

  const handleBackClick = () => {
    setViewDetails(false);
    setSelectedItem(null);
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
    <div className="history-container">
      {viewDetails ? (
        <div className="details-view">
          <button className="back-button" onClick={handleBackClick}>Back to Table</button>
          <h1>RFP Details</h1>
          <div className="details-content">
            {renderCell(selectedItem?.pdf_name) && <h2>{renderCell(selectedItem?.pdf_name)}</h2>}
            {renderCell(selectedItem?.sector) && <p><strong>Sector:</strong> {renderCell(selectedItem?.sector)}</p>}
            {renderCell(selectedItem?.dates) && <p><strong>Dates:</strong> {renderCell(selectedItem?.dates)}</p>}
            {renderCell(selectedItem?.location) && <p><strong>Location:</strong> {renderCell(selectedItem?.location)}</p>}
            {renderCell(selectedItem?.minimum_experience) && <p><strong>Minimum Experience:</strong> {renderCell(selectedItem?.minimum_experience)}</p>}
            {renderCell(selectedItem?.required_certifications) && <p><strong>Required Certifications:</strong> {renderCell(selectedItem?.required_certifications)}</p>}
            {renderCell(selectedItem?.similar_project_references) && <p><strong>Similar Project References:</strong> {renderCell(selectedItem?.similar_project_references)}</p>}
            {renderCell(selectedItem?.it_infrastructure) && <p><strong>IT Infrastructure:</strong> {renderCell(selectedItem?.it_infrastructure)}</p>}
            {renderCell(selectedItem?.network_infrastructure) && <p><strong>Network Infrastructure:</strong> {renderCell(selectedItem?.network_infrastructure)}</p>}
            {renderCell(selectedItem?.virtualization) && <p><strong>Virtualization:</strong> {renderCell(selectedItem?.virtualization)}</p>}
            {renderCell(selectedItem?.programming_languages) && <p><strong>Programming Languages:</strong> {renderCell(selectedItem?.programming_languages)}</p>}
            {renderCell(selectedItem?.cloud_computing_data_management_ai_skills) && <p><strong>Cloud Computing, Data Management, AI Skills:</strong> {renderCell(selectedItem?.cloud_computing_data_management_ai_skills)}</p>}
            {renderCell(selectedItem?.cybersecurity_devops_big_data_skills) && <p><strong>Cybersecurity, DevOps, Big Data Skills:</strong> {renderCell(selectedItem?.cybersecurity_devops_big_data_skills)}</p>}
            {renderCell(selectedItem?.iot_network_telecom_blockchain_skills) && <p><strong>IoT, Network, Telecommunications, Blockchain Skills:</strong> {renderCell(selectedItem?.iot_network_telecom_blockchain_skills)}</p>}
            {renderCell(selectedItem?.automation_orchestration_data_analysis_skills) && <p><strong>Automation, Orchestration, Data Analysis Skills:</strong> {renderCell(selectedItem?.automation_orchestration_data_analysis_skills)}</p>}
            {renderCell(selectedItem?.maintainability) && <p><strong>Requested Solution Quality:</strong> {renderCell(selectedItem?.technical_support_and_maintenance)}, {renderCell(selectedItem?.reliability)}, {renderCell(selectedItem?.flexibility)}, {renderCell(selectedItem?.integrity)}, {renderCell(selectedItem?.availability)}, {renderCell(selectedItem?.solution_scalability)}</p>}
            {renderCell(selectedItem?.project_management_approaches) && <p><strong>Project Management Approaches:</strong> {renderCell(selectedItem?.project_management_approaches)}</p>}
            {renderCell(selectedItem?.project_resources) && <p><strong>Project Resources:</strong> {renderCell(selectedItem?.project_resources)}</p>}
            {renderCell(selectedItem?.training) && <p><strong>Training:</strong> {renderCell(selectedItem?.training)}</p>}
            {renderCell(selectedItem?.deployment) && <p><strong>Deployment:</strong> {renderCell(selectedItem?.deployment)}</p>}
            {renderCell(selectedItem?.regulations) && <p><strong> Regulations:</strong> {renderCell(selectedItem?.regulations)}</p>}
            {renderCell(selectedItem?.legal_compliance) && <p><strong>Legal Compliance:</strong> {renderCell(selectedItem?.legal_compliance)}</p>}
            {renderCell(selectedItem?.score) && <p><strong>Score:</strong> {renderCell(selectedItem?.score)}%</p>}
          </div>
        </div>
      ) : (
        <div className="table-view">
          <button className="dashboard-button" onClick={handleDashboardClick}>Return to Dashboard</button>
          <h1>RFP Analysis History</h1>
          <table className="history-table">
            <thead>
              <tr>
                <th>PDF Name</th>
                <th>Analysis Date</th>
              </tr>
            </thead>
            <tbody>
              {historyData.map((item, index) => (
                <tr key={index} onClick={() => handleRowClick(item)} className="clickable-row">
                  <td>{item?.pdf_name}</td>
                  <td>{new Date(item?.creation_date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default RFPHistory;
