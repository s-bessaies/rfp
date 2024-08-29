import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom'; 
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, BarElement, LineElement, DoughnutController, PointElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import Navbar from './components/navbar2.js';
import Modal from './components/modal'; // Import the Modal component
import './home.css';

Chart.register(CategoryScale, LinearScale, BarElement, LineElement, DoughnutController, PointElement, ArcElement, Title, Tooltip, Legend);

function Home({ onLogout }) {
  const navigate = useNavigate();
  const [chartType, setChartType] = useState('bar');
  const [data, setData] = useState([]);
  const [selectedRFP, setSelectedRFP] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false); // State to control modal visibility

  const handleAnalyzeRFP = () => {
    navigate('/analyze-rfp');
  };

  useEffect(() => {
    fetch(`/process-pdf/api/rfp-history-top/?username=${localStorage.getItem('username')}`)
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
  }, []);

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

  const handleRowClick = (item) => {
    setSelectedRFP(item);
    setIsModalOpen(true); // Open the modal
  };

  const handleCloseModal = () => {
    setIsModalOpen(false); // Close the modal
  };

  const chartData = {
    labels: data.map(item => item.pdf_name),
    datasets: [
      {
        label: 'RFP Scores (%)',
        data: data.map(item => item.score), 
        backgroundColor: ['#4A90E2', '#50E3C2', '#F5A623', '#B8E986', '#BD10E0'],
        borderColor: '#ffffff',
        borderWidth: 1,
        hoverBackgroundColor: '#ffffff',
        hoverBorderColor: '#4A90E2',
      },
    ],
  };

  const renderChart = () => {
    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { 
        tooltip: {
          enabled: true,
          callbacks: {
            label: function(tooltipItem) {
              return `${tooltipItem.label}: ${tooltipItem.raw}%`;
            }
          }
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            color: '#333',
            font: {
              size: 14,
            }
          }
        },
        title: {
          display: true,
          text: 'RFP Score Overview',
          font: {
            size: 18,
            weight: 'bold',
          },
          color: '#FFF',
        }
      },
      scales: {
        x: { 
          grid: { display: false },
          ticks: {
            color: '#FFF',
            font: {
              size: 12,
            }
          },
        },
        y: {
          grid: { 
            display: true,
            color: '#e0e0e0'
          },
          ticks: {
            beginAtZero: true,
            color: '#FFF',
            font: {
              size: 12,
            },
            callback: function(value) {
              return value + '%';
            }
          }
        },
      },
    };

    switch (chartType) {
      case 'line':
        return <Line data={chartData} options={commonOptions} />;
      case 'doughnut':
        return <Doughnut data={chartData} options={commonOptions} />;
      default:
        return <Bar data={chartData} options={commonOptions} />;
    }
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="dashboard-container">
        <header className="hero-section">
          <h1 className="page-title">Welcome to the RFP Analyzer</h1>
          <p className="hero-subtitle">Streamline your RFP analysis process with ease.</p>
        </header>
        <div className="button-group">
          <button onClick={handleAnalyzeRFP} className="btn btn-analyze">Analyze an RFP</button>
        </div>
        <section className="key-metrics">
          <div className="card table-card">
            <h2 className="card-title">Best Matches</h2>
            <table className="score-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Score</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {data.map((item, index) => (
                  <tr 
                    key={index} 
                    className="clickable-row"
                    onClick={() => handleRowClick(item)}  // Open modal on row click
                  >
                    <td>
                      <Link to="#" className="table-link">{item.pdf_name}</Link>
                    </td>
                    <td>{item.score}%</td>
                    <td>{item.description || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="card chart-card">
            <h2 className="card-title">Score Overview</h2>
            <div className="chart-controls">
              <button onClick={() => setChartType('bar')}>Bar</button>
              <button onClick={() => setChartType('line')}>Line</button>
              <button onClick={() => setChartType('doughnut')}>Doughnut</button>
            </div>
            <div className="chart-container">
              {renderChart()}
            </div>
          </div>
        </section>

        {/* Modal for RFP Details */}
        <Modal isOpen={isModalOpen} onClose={handleCloseModal}>
  {selectedRFP && (
    <div className="details-section">
      <h3 className="details-title">Basic Information</h3>
      {renderCell(selectedRFP.pdf_name) && (
        <p><strong>PDF Name:</strong> {renderCell(selectedRFP.pdf_name)}</p>
      )}
      {renderCell(selectedRFP.description) && (
        <p><strong>Description:</strong> {renderCell(selectedRFP.description)}</p>
      )}
      {renderCell(selectedRFP.sector) && (
        <p><strong>Sector:</strong> {renderCell(selectedRFP.sector)}</p>
      )}
      {renderCell(selectedRFP.dates) && (
        <p><strong>Dates:</strong> {renderCell(selectedRFP.dates)}</p>
      )}
      {renderCell(selectedRFP.location) && (
        <p><strong>Location:</strong> {renderCell(selectedRFP.location)}</p>
      )}

      <h3 className="details-title">Requirements</h3>
      {renderCell(selectedRFP.minimum_experience) && (
        <p><strong>Minimum Experience:</strong> {renderCell(selectedRFP.minimum_experience)}</p>
      )}
      {renderCell(selectedRFP.required_certifications) && (
        <p><strong>Required Certifications:</strong> {renderCell(selectedRFP.required_certifications)}</p>
      )}
      {renderCell(selectedRFP.similar_project_references) && (
        <p><strong>Similar Project References:</strong> {renderCell(selectedRFP.similar_project_references)}</p>
      )}
      {renderCell(selectedRFP.it_infrastructure) && (
        <p><strong>IT Infrastructure:</strong> {renderCell(selectedRFP.it_infrastructure)}</p>
      )}
      {renderCell(selectedRFP.network_infrastructure) && (
        <p><strong>Network Infrastructure:</strong> {renderCell(selectedRFP.network_infrastructure)}</p>
      )}
      {renderCell(selectedRFP.virtualization) && (
        <p><strong>Virtualization:</strong> {renderCell(selectedRFP.virtualization)}</p>
      )}
      {renderCell(selectedRFP.programming_languages) && (
        <p><strong>Programming Languages:</strong> {renderCell(selectedRFP.programming_languages)}</p>
      )}
      {renderCell(selectedRFP.cloud_computing_data_management_ai_skills) && (
        <p><strong>Cloud Computing, Data Management & AI Skills:</strong> {renderCell(selectedRFP.cloud_computing_data_management_ai_skills)}</p>
      )}
      {renderCell(selectedRFP.cybersecurity_devops_big_data_skills) && (
        <p><strong>Cybersecurity, DevOps & Big Data Skills:</strong> {renderCell(selectedRFP.cybersecurity_devops_big_data_skills)}</p>
      )}
      {renderCell(selectedRFP.iot_network_telecom_blockchain_skills) && (
        <p><strong>IoT, Network, Telecom & Blockchain Skills:</strong> {renderCell(selectedRFP.iot_network_telecom_blockchain_skills)}</p>
      )}
      {renderCell(selectedRFP.automation_orchestration_data_analysis_skills) && (
        <p><strong>Automation, Orchestration & Data Analysis Skills:</strong> {renderCell(selectedRFP.automation_orchestration_data_analysis_skills)}</p>
      )}

      <h3 className="details-title">Project Management</h3>
      {renderCell(selectedRFP.project_management_approaches) && (
        <p><strong>Project Management Approaches:</strong> {renderCell(selectedRFP.project_management_approaches)}</p>
      )}
      {renderCell(selectedRFP.project_resources) && (
        <p><strong>Project Resources:</strong> {renderCell(selectedRFP.project_resources)}</p>
      )}
      {renderCell(selectedRFP.training) && (
        <p><strong>Training:</strong> {renderCell(selectedRFP.training)}</p>
      )}
      {renderCell(selectedRFP.deployment) && (
        <p><strong>Deployment:</strong> {renderCell(selectedRFP.deployment)}</p>
      )}

      <h3 className="details-title">Support & Maintenance</h3>
      {renderCell(selectedRFP.technical_support_and_maintenance) && (
        <p><strong>Technical Support & Maintenance:</strong> {renderCell(selectedRFP.technical_support_and_maintenance)}</p>
      )}

      <h3 className="details-title">Legal & Compliance</h3>
      {renderCell(selectedRFP.legal_compliance) && (
        <p><strong>Legal Compliance:</strong> {renderCell(selectedRFP.legal_compliance)}</p>
      )}
    </div>
  )}
</Modal>
</div>
</>
);
}

export default Home;
