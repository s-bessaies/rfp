import React from 'react';
import { motion } from 'framer-motion';
import './Features.css';

const features = [
  { 
    title: "Generative AI Analysis", 
    description: "Our AI-powered RFP Analyzer utilizes cutting-edge generative AI to deeply analyze and understand the nuances of your RFPs. It provides insights and suggestions that are tailored to your specific needs, helping you to craft more competitive and compelling proposals. The AI learns from your past submissions and continuously improves, ensuring that your responses are always top-notch." 
  },
  { 
    title: "Company Profile Matching", 
    description: "Leverage advanced AI algorithms to match your analyzed RFPs with the best-suited company profiles. Our system considers various factors such as industry, company size, past performance, and specific requirements to ensure that the proposals are directed to the right organizations. This increases your chances of success and ensures a better alignment between RFP issuers and responders." 
  },

  { 
    title: "Automated Compliance Checks", 
    description: "Ensure that your proposals meet all necessary compliance and regulatory requirements with our automated checks. The AI reviews your RFP responses for common compliance issues, flagging potential problems before submission. This reduces the risk of rejections due to non-compliance and helps you avoid costly mistakes." 
  },

];

const Features = () => {
  return (
    <div className="features-section">
      <h2>Features</h2>
      <div className="feature-cards">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            className="feature-card"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.2, duration: 0.5 }}
          >
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Features;
