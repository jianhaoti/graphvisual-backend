const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const app = express();
const port = process.env.PORT || 3001;

// Use CORS middleware to allow requests from your frontend origin
const allowedOrigins = [
  "https://graphvisual.vercel.app",
  "http://localhost:3000",
];

app.use(
  cors({
    origin: function (origin, callback) {
      // Allow requests with no origin (like mobile apps or curl requests)
      if (!origin) return callback(null, true);
      if (allowedOrigins.indexOf(origin) === -1) {
        const msg =
          "The CORS policy for this site does not allow access from the specified Origin.";
        return callback(new Error(msg), false);
      }
      return callback(null, true);
    },
  })
);

// delivery man
app.use(express.json());

// Define a POST route for the algorithm
app.post("/dijkstra", (req, res) => {
  const {
    theNeighbors,
    edgeWeightMap: edgeWeightArray,
    isOriented,
    source,
  } = req.body;

  // package it up for the script
  const pythonInput = JSON.stringify({
    theNeighbors,
    edgeWeights: edgeWeightArray, // Ensure this matches the Python script's expectations
    isOriented,
    source,
  });

  console.log(pythonInput);
  // Spawn the Python subprocess
  const pythonProcess = spawn("python3", ["dijkstras.py"]);

  // Send in data
  pythonProcess.stdin.write(pythonInput);
  pythonProcess.stdin.end(); // Indicate that no more data will be sent

  let result = ""; // Initialize an empty string to accumulate data from stdout

  // Handle data event from stdout
  pythonProcess.stdout.on("data", (data) => {
    result += data.toString(); // Append the data to the result variable
  });

  // Handle data event from stderr (log errors, if any)
  pythonProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  // Handle the close event of the subprocess
  pythonProcess.on("close", (code) => {
    if (code === 0) {
      const parsedResult = JSON.parse(result);
      res.status(200).json(parsedResult);
    } else {
      // Error
      console.error("Error parsing JSON from Python script:", error);
      res.status(500).send("Error processing Dijkstra's algorithm");
    }
  });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
