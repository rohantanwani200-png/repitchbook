const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json());

// 🔴 PASTE YOUR AI ENGINE URL HERE
const AI_URL = "https://workspace-rohantanwani200.replit.app/generate";

app.post("/create-pitch", async (req, res) => {
  try {
    // Send data to AI Engine
    const aiResponse = await axios.post(AI_URL, req.body);

    // Get slides from AI
    const slides = aiResponse.data.slides;

    // Send slides back to frontend
    res.json({ slides });
  } catch (error) {
    res.status(500).json({ error: "AI Engine not responding" });
  }
});

app.get("/", (req, res) => {
  res.send("RePitchBook Backend Running");
});

app.listen(5000, "0.0.0.0", () => {
  console.log("Backend running on port 5000");
});

