import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const SyntheticDataTestPage = () => {
  const [dataSize, setDataSize] = useState('');
  const [dataType, setDataType] = useState('JSON');
  const [testScenario, setTestScenario] = useState('');

  const handleGenerateData = () => {
    // Handle synthetic data generation logic here
    alert('Synthetic Data Generated!');
  };

  return (
    <div className="synthetic-data-test-page">
      <div className="row">
        <h4>Synthetic Data Testing</h4>
      </div>
      <div className="form">
        <input
          type="text"
          placeholder="Enter Data Size"
          value={dataSize}
          onChange={(e) => setDataSize(e.target.value)}
        />
        <select value={dataType} onChange={(e) => setDataType(e.target.value)}>
          <option value="JSON">JSON</option>
          <option value="CSV">CSV</option>
          <option value="XML">XML</option>
        </select>
        <textarea
          placeholder="Test Scenario"
          value={testScenario}
          onChange={(e) => setTestScenario(e.target.value)}
        />
        <button onClick={handleGenerateData}>Generate Data</button>
        <Link to="/"><button>Back to Home</button></Link>
      </div>
    </div>
  );
};

export default SyntheticDataTestPage;
