import express from "express";
import dotenv from "dotenv";
import { createPullRequest } from "./github.js";

dotenv.config();
const app = express();
app.use(express.json());

app.post("/pull-request", async (req, res) => {
  try {
    const prUrl = await createPullRequest(req.body);
    res.json({ pr_url: prUrl });
  } catch (err) {
    console.error("Failed to create PR:", err);
    res.status(500).json({ error: "Failed to create pull request" });
  }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`GitHub MCP server running on port ${PORT}`));