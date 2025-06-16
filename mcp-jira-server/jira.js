import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const jiraBaseUrl = process.env.JIRA_BASE_URL;
const auth = {
  username: process.env.JIRA_EMAIL,
  password: process.env.JIRA_API_TOKEN,
};

export async function getTicket(ticketId) {
  const url = `${jiraBaseUrl}/rest/api/3/issue/${ticketId}`;
  const { data } = await axios.get(url, { auth });
  const fields = data.fields;

  return {
    ticket_id: ticketId,
    summary: fields.summary,
    description: fields.description,
    repo_url: fields.customfield_12345 || "",  // replace with your custom field ID
  };
}

export async function addComment(ticketId, text) {
  const url = `${jiraBaseUrl}/rest/api/3/issue/${ticketId}/comment`;
  return await axios.post(
    url,
    { body: text },
    { auth }
  );
}

export async function updateStatus(ticketId, newStatus) {
  // You'll need to map `newStatus` to your workflow's transition ID.
  const transitionsUrl = `${jiraBaseUrl}/rest/api/3/issue/${ticketId}/transitions`;
  const { data } = await axios.get(transitionsUrl, { auth });

  const matching = data.transitions.find(t => t.name.toLowerCase() === newStatus.toLowerCase());
  if (!matching) throw new Error(`No transition matching "${newStatus}"`);

  return await axios.post(
    transitionsUrl,
    { transition: { id: matching.id } },
    { auth }
  );
}