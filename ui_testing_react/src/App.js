import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import UiTestPage from './components/UiTestPage';
import ApiTestPage from './components/ApiTestPage';
import SyntheticDataTestPage from './components/SyntheticDataTestPage';
import SettingsPage from './components/SettingsPage';
import PerformanceTestPage from './components/PerformanceTestPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/ui-test" element={<UiTestPage />} />
          <Route path="/api-test" element={<ApiTestPage />} />
          <Route path="/synthetic-data-test" element={<SyntheticDataTestPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/performance-test" element={<PerformanceTestPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
