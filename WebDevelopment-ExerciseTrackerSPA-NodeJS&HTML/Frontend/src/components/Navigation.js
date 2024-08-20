import React from 'react';
import { Link } from 'react-router-dom';


function Navigation() {
  return (
    <nav>
        <Link to="/">Home</Link>
        <Link to="../create-exercise">Create Exercise</Link>
    </nav>
  );
}

export default Navigation;
