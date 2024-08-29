import React from 'react';
import Header from './components/Header';
import Features from './components/Features';
import Pricing from './components/Pricing';
import Navbar from './components/navbar';

const WelcomePage = () => {
  return (
    <div>
        <Navbar/>
        <section id="head"><Header /></section>
      
      <section id="features">
        <Features />
      </section>
      <section id="pricing">
        <Pricing />
      </section>
      
    </div>
  );
};

export default WelcomePage;
