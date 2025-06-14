from jira_connector import JiraConnector
from github_agent import GitHubAgent
from repo_context_loader import RepoContextLoader

loader = RepoContextLoader(repo_path="./repos/BUG-123")
files = loader.list_files()
snippets = loader.extract_snippets(files)

prompt = loader.build_prompt(
    summary="Fix login timeout after 30s",
    description="When users are idle for 30s, session expires too early. Adjust the timeout logic in the auth layer.",
    snippets=snippets
)

# Now send `prompt` to Gemini

github = GitHubAgent(mcp_github_url="http://localhost:4000")  # Adjust port if needed

# 1. Clone and branch
repo_url = "https://github.com/org/repo.git"
ticket_id = "BUG-123"
repo_path = github.clone_repo(repo_url, ticket_id)
branch_name = github.create_branch(repo_path, branch_name=f"feature/{ticket_id}")

# 2. Generate code (via Gemini) and write to a file (done elsewhere)

# 3. Open PR via MCP
pr_url = github.open_pr(
    repo_url=repo_url,
    branch_name=branch_name,
    base="main",
    title=f"[{ticket_id}] Fix login timeout",
    body="This PR addresses the issue described in Jira ticket BUG-123."
)
print(f"Pull Request created: {pr_url}")

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