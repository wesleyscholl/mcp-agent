import express from "express";
import dotenv from "dotenv";
import { getTicket, addComment, updateStatus } from "./jira.js";

dotenv.config();
const app = express();
app.use(express.json());

app.get("/tickets/:id", async (req, res) => {
  try {
    const ticket = await getTicket(req.params.id);
    res.json(ticket);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to fetch ticket" });
  }
});

app.post("/tickets/:id/comment", async (req, res) => {
  try {
    await addComment(req.params.id, req.body.text);
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to post comment" });
  }
});

app.put("/tickets/:id/status", async (req, res) => {
  try {
    await updateStatus(req.params.id, req.body.status);
    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to update status" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Jira MCP server running on port ${PORT}`));