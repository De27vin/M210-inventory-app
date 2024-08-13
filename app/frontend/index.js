/**
 * index.js
 *
 * This Express application serves a static frontend and provides an API route 
 * to deliver configuration data to the frontend. The server listens on a specified 
 * port and serves the index.html file for all other requests.
 *
 * Dependencies:
 * - express: Web framework for Node.js.
 * - path: Node.js module for handling and transforming file paths.
 *
 * Configuration:
 * - PORT: The port on which the server will listen (defaults to 3000 if not set).
 * - BACKEND_PROTOCOL: Protocol for the backend server (defaults to 'http').
 * - BACKEND_HOST: Hostname for the backend server (defaults to 'localhost').
 * - BACKEND_PORT: Port for the backend server (defaults to 5001).
 *
 * Routes:
 * - /api/config: Provides configuration data to the frontend.
 * - *: Serves the index.html file for all other requests.
 */
const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Middleware to serve static files (e.g., frontend files)
app.use(express.static(path.join(__dirname, 'public')));

// API route to provide configuration data
app.get('/api/config', (req, res) => {
    // Providing environment variables to the frontend
    res.json({
        BACKEND_PROTOCOL: process.env.BACKEND_PROTOCOL || 'http',
        BACKEND_HOST: process.env.BACKEND_HOST || 'localhost',
        BACKEND_PORT: process.env.BACKEND_PORT || '5001'
    });
});

// Route for all other requests to serve the index.html file
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
