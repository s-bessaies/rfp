import React from 'react';
import './Pricing.css';
import CTA from './CTA';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation

const pricingPlans = [
  { 
    title: "Basic Plan", 
    price: "$29/month", 
    description: "Perfect for small businesses just getting started. Includes basic AI analysis and template customization features.",
    features: ["Generative AI Analysis", "Company Profile Matching", "Email Support"]
  },
  { 
    title: "Pro Plan", 
    price: "$79/month", 
    description: "Ideal for growing companies that need more advanced AI capabilities and real-time collaboration features.",
    features: ["All Basic Plan Features", "Customizable Templates", "Real-Time Collaboration", "Priority Support"]
  },
  { 
    title: "Enterprise Plan", 
    price: "Contact Us", 
    description: "For large organizations with extensive RFP needs. Get full access to all features, customized solutions, and dedicated support.",
    features: ["All Pro Plan Features", "Automated Compliance Checks", "Data-Driven Insights", "Dedicated Account Manager"]
  },
];

const Pricing = () => {
    
const navigate = useNavigate(); 
const handleSubscribe = () => {
    navigate('/form'); 
  };
  return (
    <div className="pricing-section">
      <h2>Pricing Plans</h2>
      <div className="pricing-cards">
        {pricingPlans.map((plan, index) => (
          <div key={index} className="pricing-card">
            <h3>{plan.title}</h3>
            <p className="price">{plan.price}</p>
            <p>{plan.description}</p>
            <ul>
              {plan.features.map((feature, idx) => (
                <li key={idx}>{feature}</li>
              ))}
            </ul>
            <button className="select-plan">Select Plan</button>
          </div>
        ))}
      </div>
      <CTA text="Subscribe Now" onClick={handleSubscribe} size="large" />
    </div>
  );
};

export default Pricing;
