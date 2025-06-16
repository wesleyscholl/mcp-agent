import os
import requests

class JiraConnector:
    def __init__(self, mcp_base_url: str):
        self.base_url = mcp_base_url.rstrip("/")
        self.headers = {
            "Content-Type": "application/json"
        }

    def get_ticket(self, ticket_id: str):
        """Fetch ticket metadata from the MCP Jira server."""
        url = f"{self.base_url}/tickets/{ticket_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_comment(self, ticket_id: str, comment: str):
        """Add a comment to a ticket via MCP Jira server."""
        url = f"{self.base_url}/tickets/{ticket_id}/comment"
        payload = {"text": comment}
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_status(self, ticket_id: str, status: str):
        """Update Jira ticket status (e.g., In Progress, Done)."""
        url = f"{self.base_url}/tickets/{ticket_id}/status"
        payload = {"status": status}
        response = requests.put(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
