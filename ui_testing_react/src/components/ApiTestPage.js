import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const ApiTestPage = () => {
  const [swaggerFile, setSwaggerFile] = useState(null);
  const [endpoints, setEndpoints] = useState([]);
  const [additionalInputs, setAdditionalInputs] = useState('');
  const [framework, setFramework] = useState('Python Pytest');

  const handleFileChange = (e) => {
    setSwaggerFile(e.target.files[0]);
  };

  const handleSubmit = () => {
    // Handle API test generation logic here
    alert('API Test Generated!');
  };

  return (
    <div className="api-test-page">
      <div className="row">
        <h4>API Testing</h4>
      </div>
      <div className="form">
        <input type="file" onChange={handleFileChange} />
        <textarea
          placeholder="Additional Inputs"
          value={additionalInputs}
          onChange={(e) => setAdditionalInputs(e.target.value)}
        />
        <select value={framework} onChange={(e) => setFramework(e.target.value)}>
          <option value="Python Pytest">Python Pytest</option>
          <option value="Cypress">Cypress</option>
          <option value="Karate">Karate</option>
        </select>
        <button onClick={handleSubmit}>Submit</button>
        <Link to="/"><button>Back to Home</button></Link>
      </div>
    </div>
  );
};

export default ApiTestPage;
