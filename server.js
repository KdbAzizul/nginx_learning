const express = require('express'); // Import the express module
const app = express(); // Create an Express application instance
const port = 3000; // Define the port number


const appId = process.env.APP_ID || 'Unknown Instance';
// Define a route for GET requests to the root URL
app.get('/', (req, res) => {
  res.send(`Hello World from ${appId}!`); // Send a unique response
});

// Start the server and listen for incoming connections
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
 