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

// POST for dijkstra
app.post("/dijkstra", (req, res) => {
  const {
    graphAdjacencyList,
    edgeWeightMap: edgeWeightArray,
    isOriented,
    source,
  } = req.body;

  // package it up for the script
  const pythonInput = JSON.stringify({
    graphAdjacencyList,
    edgeWeights: edgeWeightArray, // Ensure this matches the Python script's expectations
    isOriented,
    source,
  });
  //   console.log("Python Input:", pythonInput);

  // Spawn the Python subprocess
  const pythonProcess = spawn("python3", ["dijkstras.py"]);

  // Send in data
  pythonProcess.stdin.write(pythonInput);
  pythonProcess.stdin.end(); // Indicate that no more data will be sent

  let result = ""; // Initialize an empty string to accumulate data from stdout

  // Handle data event from stdout
  pythonProcess.stdout.on("data", (data) => {
    // console.log("Raw output from Python script:", data.toString());
    result += data.toString();
  });

  // Handle data event from stderr (log errors, if any)
  pythonProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data.toString()}`);
  });

  // Handle the close event of the subprocess
  pythonProcess.on("close", (code) => {
    if (code === 0) {
      try {
        const parsedResult = JSON.parse(result);
        console.log("Success! Dijjkstra Steps:", parsedResult);

        res.status(200).json(parsedResult);
      } catch (error) {
        // Correctly catch and log JSON parsing errors
        console.error("Error parsing JSON from Python script:", error);
        res
          .status(500)
          .send(
            "Error processing Dijkstra's algorithm due to JSON parsing error."
          );
      }
    } else {
      // Log a generic error message or include more details if available
      console.error("Python script exited with code", code);
      //   console.error("test?");
      res.status(500).send("Error processing Dijkstra's algorithm");
    }
  });
});

// POST for prims
app.post("/prims", (req, res) => {
  const {
    graphAdjacencyList,
    edgeWeightMap: edgeWeightArray,
    source,
  } = req.body;

  // package it up for the script
  const pythonInput = JSON.stringify({
    graphAdjacencyList,
    edgeWeights: edgeWeightArray, // Ensure this matches the Python script's expectations
    source,
  });

  // console.log(pythonInput);

  // Spawn the Python subprocess
  const pythonProcess = spawn("python3", ["prims.py"]);

  // Send in data
  pythonProcess.stdin.write(pythonInput);
  pythonProcess.stdin.end(); // Indicate that no more data will be sent

  let result = ""; // Initialize an empty string to accumulate data from stdout

  // Handle data event from stdout
  pythonProcess.stdout.on("data", (data) => {
    // console.log("Raw output from Python script:", data.toString());
    result += data.toString();
  });

  // Handle data event from stderr (log errors, if any)
  pythonProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data.toString()}`);
  });

  // Handle the close event of the subprocess
  pythonProcess.on("close", (code) => {
    if (code === 0) {
      try {
        const parsedResult = JSON.parse(result);
        console.log("Success! Prims Steps:", parsedResult);

        res.status(200).json(parsedResult);
      } catch (error) {
        // Correctly catch and log JSON parsing errors
        console.error("Error parsing JSON from Python script:", error);
        res
          .status(500)
          .send("Error processing Prims' algorithm due to JSON parsing error.");
      }
    } else {
      // Log a generic error message or include more details if available
      console.error("Python script exited with code", code);
      //   console.error("test?");
      res.status(500).send("Error processing Prims' algorithm");
    }
  });
});
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
