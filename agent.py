import os
from dotenv import load_dotenv

from jira_connector import JiraConnector
from github_agent import GitHubAgent
from repo_context_loader import RepoContextLoader
from gemini_coder import GeminiCoder
from mcp_context_store import MCPContextStore

# Load environment variables
load_dotenv()

# --- Init components ---
JIRA_MCP_URL = os.getenv("JIRA_MCP_URL", "http://localhost:3000")
GITHUB_MCP_URL = os.getenv("GITHUB_MCP_URL", "http://localhost:4000")
POSTGRES_URL = os.getenv("POSTGRES_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

jira = JiraConnector(JIRA_MCP_URL)
github = GitHubAgent(GITHUB_MCP_URL)
store = MCPContextStore(POSTGRES_URL)
coder = GeminiCoder(api_key=GEMINI_API_KEY)

# --- Step 1: Accept ticket ID ---
ticket_id = input("Enter Jira ticket ID (e.g. BUG-123): ").strip()

# --- Step 2: Get ticket from Jira MCP ---
ticket = jira.get_ticket(ticket_id)
summary = ticket.get("summary")
description = ticket.get("description")
repo_url = ticket.get("repo_url")  # Jira MCP must include this field

# --- Step 3: Clone repo & create branch ---
repo_path = github.clone_repo(repo_url, ticket_id)
branch_name = github.create_branch(repo_path, branch_name=f"feature/{ticket_id}")

# --- Step 4: Analyze files (build code context) ---
loader = RepoContextLoader(repo_path=repo_path)
files = loader.list_files()
snippets = loader.extract_snippets(files)
prompt = loader.build_prompt(summary, description, snippets)

# --- Step 5: Generate + apply code ---
output_code = coder.generate_code(prompt)
relative_output_path = f"feature/{ticket_id}_fix.py"
output_file = coder.write_code_to_file(output_code, repo_path, relative_output_path)

# --- Step 6: Commit + open PR via GitHub MCP ---
pr_url = github.open_pr(
    repo_url=repo_url,
    branch_name=branch_name,
    base="main",
    title=f"[{ticket_id}] {summary}",
    body=description
)

# --- Step 7: Post PR link to Jira ---
jira.post_comment(ticket_id, f"✅ PR created: {pr_url}")
jira.update_status(ticket_id, "In Review")

# --- Step 8: Save context to PostgreSQL MCP store ---
store.insert_or_update_context(
    ticket_id=ticket_id,
    repo_url=repo_url,
    summary=summary,
    description=description,
    branch_name=branch_name,
    pr_url=pr_url,
    status="pr_created"
)

print(f"\n🎉 All done! PR created: {pr_url}")