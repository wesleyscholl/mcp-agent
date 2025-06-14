from jira_connector import JiraConnector
from github_agent import GitHubAgent
from repo_context_loader import RepoContextLoader
from gemini_coder import GeminiCoder
from mcp_context_store import MCPContextStore
import os

store = MCPContextStore(db_url=os.getenv("POSTGRES_URL"))

# Insert or update full context
store.insert_or_update_context(
    ticket_id="BUG-123",
    repo_url="https://github.com/org/repo.git",
    branch_name="feature/BUG-123",
    summary="Fix login timeout",
    description="Login session times out after 30s of inactivity"
)

# Update just status
store.update_status("BUG-123", "in_progress")

# Update just PR link
store.update_pr_url("BUG-123", "https://github.com/org/repo/pull/42")

# Retrieve current context
ctx = store.get_context("BUG-123")
print(ctx)

gemini = GeminiCoder(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Get prompt from RepoContextLoader
prompt = loader.build_prompt(summary, description, snippets)

# 2. Generate code
generated_code = gemini.generate_code(prompt)

# 3. Write it to file
output_path = gemini.write_code_to_file(
    output_code=generated_code,
    repo_path=repo_path,
    relative_path="feature/BUG-123_fix.py"
)

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