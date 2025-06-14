from jira_connector import JiraConnector

jira = JiraConnector(mcp_base_url="http://localhost:3000")  # Replace with your actual MCP Jira URL

# 1. Get ticket info
ticket_id = "BUG-123"
ticket = jira.get_ticket(ticket_id)
print("Summary:", ticket.get("summary"))
print("Description:", ticket.get("description"))

# 2. Post a comment
jira.post_comment(ticket_id, "Working on this now. PR will follow.")

# 3. Update status
jira.update_status(ticket_id, "In Progress")