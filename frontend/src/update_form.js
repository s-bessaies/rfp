import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './form.css'; // Import CSS for styling
import { useNavigate } from 'react-router-dom';

function UpdateInformation() {
  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({
    company_name: 'Innovatech Solutions Ltd.',
    headquarters_location: 'San Francisco, CA',
    year_established: 2010,
    company_size: 250,
    revenue_last_year: '35 million USD',
    ownership_structure: 'Private',
    sector_of_activity: [
      { 
        sector: 'Information Technology', 
        subsectors: ['Software Development', 'Cloud Computing', 'Cybersecurity'] 
      },
      { 
        sector: 'Telecommunications', 
        subsectors: ['Networking', 'VoIP', '5G Solutions'] 
      },
      { 
        sector: 'Financial Services', 
        subsectors: ['FinTech Solutions', 'Blockchain Development'] 
      }
    ],
    years_of_experience: 14,
    projects: [
      { scope: 'Cloud Infrastructure Setup', client: 'GlobalBank Ltd', deliverables: 'AWS Cloud Infrastructure, Security Policies' },
      { scope: 'E-commerce Platform Development', client: 'Retail Giant Inc.', deliverables: 'Online Store, Payment Integration' },
      { scope: 'Cybersecurity Audit', client: 'HealthCare Solutions', deliverables: 'Security Assessment, ISO 27001 Compliance' }
    ],
    certifications: ['ISO 27001', 'CMMI Level 3', 'AWS Certified Solutions Architect', 'Certified Information Systems Security Professional (CISSP)'],
    skills: [
      { skill_category: 'Programming Languages', skill: 'Python' },
      { skill_category: 'Cloud Computing', skill: 'AWS' },
      { skill_category: 'Cybersecurity', skill: 'ISO 27001' },
      { skill_category: 'Networking', skill: 'Cisco Certified Network Professional (CCNP)' },
      { skill_category: 'DevOps', skill: 'Docker & Kubernetes' },
      { skill_category: 'Data Science', skill: 'Machine Learning with Python' }
    ],
    it: [
      { it_category: 'Network Infrastructure', resource: 'Cisco Meraki' },
      { it_category: 'Hardware Resources', resource: 'HP ProLiant Servers' },
      { it_category: 'Security Measures', resource: 'Palo Alto Firewalls' },
      { it_category: 'Virtualization', resource: 'VMware vSphere' }
    ],
    csr_policy: 'Our CSR policy emphasizes tech education and sustainability initiatives.',
    environmental_commitment: 'We are dedicated to reducing electronic waste and increasing energy efficiency in our data centers.',
    username: '',
    password: '',
    showPassword: false,
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const skillCategories = [
    'Enterprise Application Competencies',
    'Programming Languages Skills',
    'Cloud & AI Skills',
    'Cybersecurity and Data Management Skills',
    'Project Management Methodologies',
    'Specialized Competencies',
    'Quality Assurance Processes',
    'Other Skills'
  ];
  const itCategories = [
    'Hardware resources',
    'Software and platforms',
    'Network infrastructure',
    'Security measures',
    'Scalability & flexibility',
    'Disaster recovery and business continuity',
    'Support and maintenance',
  ];
  const handleDynamicChange = (index, e, field) => {
    const { name, value } = e.target;
    const updatedField = [...formData[field]];
    updatedField[index][name] = value;
    setFormData({
      ...formData,
      [field]: updatedField
    });
  };

  const handleSkillChange = (index, e) => {
    const { name, value } = e.target;
    const updatedSkills = [...formData.skills];
    updatedSkills[index][name] = value;
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };

  const handleItChange = (index, e) => {
    const { name, value } = e.target;
    const updatedIt = [...formData.it];
    updatedIt[index][name] = value;
    setFormData({
      ...formData,
      it: updatedIt
    });
  };

  const addItField = () => {
    setFormData({
      ...formData,
      it: [...formData.it, { it_category: '', resource: '' }]
    });
  };

  const addSkillField = () => {
    setFormData({
      ...formData,
      skills: [...formData.skills, { skill_category: '', skill: '' }]
    });
  };

  const removeSkillField = (index) => {
    const updatedSkills = [...formData.skills];
    updatedSkills.splice(index, 1);
    setFormData({
      ...formData,
      skills: updatedSkills
    });
  };
  
  const removeItField = (index) => {
    const updatedIt = [...formData.it];
    updatedIt.splice(index, 1);
    setFormData({
      ...formData,
      it: updatedIt
    });
  };

  const handleArrayChange = (index, e, field) => {
    const updatedField = [...formData[field]];
    updatedField[index] = e.target.value;
    setFormData({
      ...formData,
      [field]: updatedField
    });
  };
  const handleSubsectorChange = (index, subIndex, e) => {
    const { value } = e.target;
    const updatedField = [...formData.sector_of_activity];
    updatedField[index].subsectors[subIndex] = value;
    setFormData({
      ...formData,
      sector_of_activity: updatedField
    });
  };
  
  const addSubsector = (index) => {
    const updatedField = [...formData.sector_of_activity];
    updatedField[index].subsectors.push('');
    setFormData({
      ...formData,
      sector_of_activity: updatedField
    });
  };
  
  const removeSubsector = (index, subIndex) => {
    const updatedField = [...formData.sector_of_activity];
    updatedField[index].subsectors.splice(subIndex, 1);
    setFormData({
      ...formData,
      sector_of_activity: updatedField
    });
  };
  
  const addField = (field) => {
    setFormData({
      ...formData,
      [field]: [...formData[field], field === 'projects' ? { scope: '', client: '', deliverables: '' } : '']
    });
  };

  const removeField = (index, field) => {
    const updatedField = [...formData[field]];
    updatedField.splice(index, 1);
    setFormData({
      ...formData,
      [field]: updatedField
    });
  };
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  useEffect(() => {
    if (username) {
      const fetchData = async () => {
        try {
          const response = await axios.get(`/company/api/get-info/${username}/`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
          });
          console.log(response.data)
          setFormData(response.data);
        } catch (error) {
          console.error('Error fetching data:', error.response ? error.response.data : error.message);
          setError('Failed to fetch data.');
        }
      };

      fetchData();
    } else {
      setError('Username not found in local storage.');
    }
  }, [username]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  const handleReturn = () =>{
    navigate('/'); 
  }
  const handleUpdateRedirect = async (e) => {
    console.log(formData)
    e.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      const response = await axios.put(`/company/api/update-info/${username}/`, formData, {
        headers: {
          'Content-Type': 'application/json',
        }
      });

      setSuccess(true);
      setFormData({
        username: '',
        password: '',
        company_name: '',
        headquarters_location: '',
        year_established: 2000,
        company_size: 100,
        revenue_last_year: '',
        ownership_structure: '',
        sector_of_activity: [
          { 
            sector: '', 
            subsectors: [''] 
          }
        ],
        years_of_experience: 10,
        projects: [{ scope: '', client: '', deliverables: '' }],
        certifications: [''],
        skills: [{ skill_category: '', skill: '' }],
        it: [{ it_category: '', resource: '' }],
        csr_policy: '',
        environmental_commitment: ''
      });
      navigate('/');
    } catch (error) {
      setError('Failed to submit the form. Please try again.');
    }
    navigate('/login'); 
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      const response = await axios.put(`/company/api/update-info/${username}/`, formData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        }
      });

      console.log('Response:', response.data);
      setSuccess(true);
      navigate('/'); 
    } catch (error) {
      console.error('Error updating data:', error.response ? error.response.data : error.message);
      setError('Failed to update information. Please try again.');
    }
  };

  return (
    <div className="form-container">
      {/* Username Field */}
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

  {/* Password Field */}
    <div className="form-group">
      <label htmlFor="password">Password:</label>
      <div className="password-container">
        <input
          type={showPassword ? 'text' : 'password'}
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="button" onClick={() => setShowPassword(!showPassword)} className="toggle-password add-button">
          {showPassword ? 'Hide' : 'Show'}
        </button>
      </div>
    </div>
      <h2>Company Profile</h2>
      {success && <div className="success-message">Form submitted successfully!</div>}
      {error && <div className="error-message">{error}</div>}
      <form>
        {/* Company Profile Section */}
        <div className="form-group">
          <label htmlFor="company_name">Company Name:</label>
          <input
            type="text"
            id="company_name"
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="headquarters_location">Headquarters Location:</label>
          <input
            type="text"
            id="headquarters_location"
            name="headquarters_location"
            value={formData.headquarters_location}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="year_established">Year Established:</label>
          <input
            type="range"
            id="year_established"
            name="year_established"
            min="1900"
            max={new Date().getFullYear()}
            value={formData.year_established}
            onChange={handleChange}
            required
          />
          <span>{formData.year_established}</span>
        </div>

        <div className="form-group">
          <label htmlFor="company_size">Company Size:</label>
          <input
             type="range"
             id="company_size"
             name="company_size"
             min="1"
             max="10000"
             value={formData.company_size}
             onChange={handleChange}
          />
          <span>{formData.company_size}</span>
        </div>
        <div className="form-group">
          <label htmlFor="years_of_experience">Years of Experience:</label>
          <input
            type="range"
            id="years_of_experience"
            name="years_of_experience"
            min="0"
            max="100"
            value={formData.years_of_experience}
            onChange={handleChange}
            required
          />
           <span>{formData.years_of_experience}</span>
        </div>
        <div className="form-group">
          <label htmlFor="revenue_last_year">Revenue Last Year:</label>
          <input
            type="text"
            id="revenue_last_year"
            name="revenue_last_year"
            value={formData.revenue_last_year}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="ownership_structure">Ownership Structure:</label>
          <input
            type="text"
            id="ownership_structure"
            name="ownership_structure"
            value={formData.ownership_structure}
            onChange={handleChange}
          />
        </div>

        <h2>Sector of Activity</h2>
{formData.sector_of_activity.map((industry, index) => (
  <div key={index} className="form-group industry-group">
    <div className="sector-header">
      <label htmlFor={`sector-${index}`}><strong>Sector:</strong></label>
      <input
        type="text"
        id={`sector-${index}`}
        name="sector"
        value={industry.sector}
        onChange={(e) => handleDynamicChange(index, e, 'sector_of_activity')}
        required
        className="sector-input"
      />
      <button type="button" onClick={() => removeField(index, 'sector_of_activity')} className="add-button">Remove Sector</button>
    </div>

    <div className="subsectors-section">
      <label><strong>Subsectors:</strong></label>
      {industry.subsectors.map((subsector, subIndex) => (
        <div key={subIndex} className="form-group subsector-group">
          <input
            type="text"
            id={`subsector-${index}-${subIndex}`}
            name="subsectors"
            value={subsector}
            onChange={(e) => handleSubsectorChange(index, subIndex, e)}
            required
            className="subsector-input"
          />
          <button type="button" onClick={() => removeSubsector(index, subIndex)} className="add-button">Remove</button>
        </div>
      ))}
      <button type="button" onClick={() => addSubsector(index)} className="add-button">Add Subsector</button>
    </div>
  </div>
))}
<button type="button" className="add-button" onClick={() => addField('sector_of_activity')}>Add Another Sector</button>




        

        {/* Dynamic Projects Section */}
        <h2>Notable Clients and Projects</h2>
        {formData.projects.map((project, index) => (
          <div key={index} className="form-group project-group">
            <label htmlFor={`scope-${index}`}>Project Scope:</label>
            <input
              type="text"
              id={`scope-${index}`}
              name="scope"
              value={project.scope}
              onChange={(e) => handleDynamicChange(index, e, 'projects')}
              required
            />
            <label htmlFor={`client-${index}`}>Client:</label>
            <input
              type="text"
              id={`client-${index}`}
              name="client"
              value={project.client}
              onChange={(e) => handleDynamicChange(index, e, 'projects')}
              required
            />
            <label htmlFor={`deliverables-${index}`}>Deliverables:</label>
            <input
              type="text"
              id={`deliverables-${index}`}
              name="deliverables"
              value={project.deliverables}
              onChange={(e) => handleDynamicChange(index, e, 'projects')}
              required
            />
            <button type="button" onClick={() => removeField(index, 'projects')} className="add-button">Remove Project</button>
          </div>
        ))}
        <button type="button" className="add-button" onClick={() => addField('projects')}>Add Another Project</button>

        {/* Dynamic IT Infrastructure Section */}
        <h2>IT Infrastructure</h2>
        {formData.it.map((it, index) => (
          <div key={index} className="form-group">
            <label htmlFor={`it_category-${index}`}>IT Category:</label>
            <select
              id={`it_category-${index}`}
              name="it_category"
              value={it.it_category}
              onChange={(e) => handleItChange(index, e)}
              required
            >
              <option value="">Select Category</option>
              {itCategories.map((category, i) => (
                <option key={i} value={category}>{category}</option>
              ))}
            </select>
            <label htmlFor={`it-${index}`}>Resource:</label>
            <input
              type="text"
              id={`it-${index}`}
              name="resource"
              value={it.resource}
              onChange={(e) => handleItChange(index, e)}
              required
            />
            <button type="button" onClick={() => removeItField(index)} className="add-button">Remove Resource</button>
          </div>
        ))}
        <button type="button" className="add-button" onClick={addItField}>Add Another Resource</button>

        {/* Dynamic Certifications Section */}
        <h2>Certifications</h2>
        {formData.certifications.map((certification, index) => (
          <div key={index} className="form-group certification-group">
            <label htmlFor={`certification-${index}`}>Certification Label:</label>
            <input
              type="text"
              id={`certification-${index}`}
              value={certification}
              onChange={(e) => handleArrayChange(index, e, 'certifications')}
              required
            />
            <button type="button" onClick={() => removeField(index, 'certifications')} className="add-button">Remove Certification</button>
          </div>
        ))}
        <button type="button" className="add-button" onClick={() => addField('certifications')}>Add Another Certification</button>
        
        {/* Dynamic Skills Section */}
        <h2>Skills</h2>
        {formData.skills.map((skill, index) => (
          <div key={index} className="form-group skill-group">
            <label htmlFor={`skill_category-${index}`}>Skill Category:</label>
            <select
              id={`skill_category-${index}`}
              name="skill_category"
              value={skill.skill_category}
              onChange={(e) => handleSkillChange(index, e)}
              required
            >
              <option value="">Select Category</option>
              {skillCategories.map((category, i) => (
                <option key={i} value={category}>{category}</option>
              ))}
            </select>
            <label htmlFor={`skill-${index}`}>Skill:</label>
            <input
              type="text"
              id={`skill-${index}`}
              name="skill"
              value={skill.skill}
              onChange={(e) => handleSkillChange(index, e)}
              required
            />
            <button type="button" onClick={() => removeSkillField(index)} className="add-button">Remove Skill</button>
          </div>
        ))}
        <button type="button" className="add-button" onClick={addSkillField}>Add Another Skill</button>

        {/* CSR Policy Section */}
        <h2>CSR Policy</h2>
        <div className="form-group">
          <label htmlFor="csr_policy">CSR Policy:</label>
          <textarea
            id="csr_policy"
            name="csr_policy"
            value={formData.csr_policy}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="environmental_commitment">Environmental Commitment:</label>
          <textarea
            id="environmental_commitment"
            name="environmental_commitment"
            value={formData.environmental_commitment}
            onChange={handleChange}
            required
          />
        </div>

      <div className="button-container">
        <button type="submit" onClick={handleUpdateRedirect} className="subscribe">Update Informations</button>
        <button type="button" onClick={handleReturn} className="comeback">Come Back</button>
      </div>

    </form>
  </div>
  );
}

export default UpdateInformation;
