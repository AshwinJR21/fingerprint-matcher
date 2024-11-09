import React from 'react';
import { Link } from 'react-router-dom';
import './navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar-links">
        <li><Link to="/">HOME</Link></li>
        <li><Link to="/sift">SIFT</Link></li>
        <li><Link to="/snn">SNN</Link></li>
        <li><Link to="/snn+">SNN+</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
