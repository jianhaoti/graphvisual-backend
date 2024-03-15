const express = require("express");
const app = express();
const port = process.env.PORT || 3001;

// Middleware to parse JSON request bodies
app.use(express.json());

// Define a POST route for the algorithm
app.post("/run-dijkstra", (req, res) => {
  console.log(req.body); // Log the request body to see the data sent
  res.status(200).send("Processing complete"); // Placeholder response
});
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
