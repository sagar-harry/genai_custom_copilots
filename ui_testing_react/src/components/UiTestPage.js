import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const UiTestPage = () => {
  const [acceptanceCriteria, setAcceptanceCriteria] = useState('');
  const [locators, setLocators] = useState('');
  const [testFramework, setTestFramework] = useState('Selenium');
  const [language, setLanguage] = useState('Python');
  const [additionalDetails, setAdditionalDetails] = useState('');

  const handleSubmit = () => {
    // Call your function to generate the test code or handle form submission.
    alert('Test code generated!');
  };

  return (
    <div className="ui-test-page">
      <div className="row">
        <h4>UI Testing</h4>
      </div>
      <div className="form">
        <textarea
          placeholder="Enter Acceptance Criteria"
          value={acceptanceCriteria}
          onChange={(e) => setAcceptanceCriteria(e.target.value)}
        />
        <textarea
          placeholder="Enter Locators"
          value={locators}
          onChange={(e) => setLocators(e.target.value)}
        />
        <textarea
          placeholder="Enter Additional Details"
          value={additionalDetails}
          onChange={(e) => setAdditionalDetails(e.target.value)}
        />
        <div>
          <select value={testFramework} onChange={(e) => setTestFramework(e.target.value)}>
            <option value="Selenium">Selenium</option>
            <option value="Cypress">Cypress</option>
            <option value="Playwright">Playwright</option>
          </select>
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="Python">Python</option>
            <option value="JavaScript">JavaScript</option>
            <option value="Java">Java</option>
            <option value="TypeScript">TypeScript</option>
          </select>
        </div>
        <button onClick={handleSubmit}>Submit</button>
        <Link to="/"><button>Back to Home</button></Link>
      </div>
    </div>
  );
};

export default UiTestPage;
