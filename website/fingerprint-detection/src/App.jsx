import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/navbar';
import Home from './pages/home'
import Siftpage from './pages/siftpage';
import Snnpage from './pages/snnpage';
import Snnpluspage from './pages/snnpluspage';
import './App.css';

const App = () => {
  return (
    <Router>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home> </Home>}></Route>
          <Route path="/sift" element={<Siftpage />} />
          <Route path="/snn" element={<Snnpage />} />
          <Route path="/snn+" element={<Snnpluspage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
