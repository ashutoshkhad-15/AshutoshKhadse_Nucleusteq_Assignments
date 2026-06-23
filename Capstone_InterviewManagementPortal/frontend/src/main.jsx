import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

// Remove the default Vite CSS import (index.css) to keep it strictly clean
// import './index.css'; 

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);