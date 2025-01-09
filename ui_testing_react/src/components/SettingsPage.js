import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const SettingsPage = () => {
  const [settingOne, setSettingOne] = useState('');
  const [settingTwo, setSettingTwo] = useState('');

  const handleSaveSettings = () => {
    // Handle saving settings logic
    alert('Settings Saved!');
  };

  return (
    <div className="settings-page">
      <div className="row">
        <h4>Settings</h4>
      </div>
      <div className="form">
        <input
          type="text"
          placeholder="Setting One"
          value={settingOne}
          onChange={(e) => setSettingOne(e.target.value)}
        />
        <input
          type="text"
          placeholder="Setting Two"
          value={settingTwo}
          onChange={(e) => setSettingTwo(e.target.value)}
        />
        <button onClick={handleSaveSettings}>Save Settings</button>
        <Link to="/"><button>Back to Home</button></Link>
      </div>
    </div>
  );
};

export default SettingsPage;
