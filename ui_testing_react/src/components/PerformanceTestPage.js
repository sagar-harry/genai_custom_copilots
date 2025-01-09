import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const PerformanceTestPage = () => {
  const [testType, setTestType] = useState('Load Test');
  const [requests, setRequests] = useState('');
  const [duration, setDuration] = useState('');
  const [additionalDetails, setAdditionalDetails] = useState('');

  const handleSubmit = () => {
    // Handle performance test logic here
    alert('Performance Test Started!');
  };

  return (
    <div className="performance-test-page">
      <div className="row">
        <h4>Performance Testing</h4>
      </div>
      <div className="form">
        <textarea
          placeholder="Enter Requests"
          value={requests}
          onChange={(e) => setRequests(e.target.value)}
        />
        <textarea
          placeholder="Enter Duration"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
        />
        <textarea
          placeholder="Additional Details"
          value={additionalDetails}
          onChange={(e) => setAdditionalDetails(e.target.value)}
        />
        <select value={testType} onChange={(e) => setTestType(e.target.value)}>
          <option value="Load Test">Load Test</option>
          <option value="Stress Test">Stress Test</option>
          <option value="Spike Test">Spike Test</option>
        </select>
        <button onClick={handleSubmit}>Start Test</button>
        <Link to="/"><button>Back to Home</button></Link>
      </div>
    </div>
  );
};

export default PerformanceTestPage;
