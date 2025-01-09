import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="home-page">
      <div className="logos">
        <div className="left-logo">
          <img src="/assets/accion.png" alt="Left Logo" style={{ height: '30px', width: 'auto' }} />
        </div>
        <div className="right-logo">
          <img src="/assets/client.png" alt="Right Logo" style={{ height: '60px', width: 'auto' }} />
        </div>
      </div>
      <h4 className="title">Testing Application</h4>
      <div className="buttons">
        <Link to="/ui-test"><button>UI Test</button></Link>
        <Link to="/api-test"><button>API Test</button></Link>
        <Link to="/synthetic-data-test"><button>Synthetic Data Test</button></Link>
        <Link to="/settings"><button>Settings</button></Link>
        <Link to="/performance-test"><button>Performance Test</button></Link>
      </div>
    </div>
  );
};

export default HomePage;
