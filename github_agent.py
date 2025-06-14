import os
import git
import tempfile
import requests

class GitHubAgent:
    def __init__(self, mcp_github_url: str):
        self.mcp_url = mcp_github_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}

    def clone_repo(self, repo_url: str, ticket_id: str) -> str:
        """Clone the repo and return the local path."""
        local_path = tempfile.mkdtemp(prefix=f"repo_{ticket_id}_")
        repo = git.Repo.clone_from(repo_url, local_path)
        return local_path

    def create_branch(self, repo_path: str, branch_name: str = None) -> str:
        """Create and switch to a new branch in the local repo."""
        repo = git.Repo(repo_path)
        branch_name = branch_name or f"feature/{repo.head.commit.hexsha[:6]}"
        repo.git.checkout('-b', branch_name)
        return branch_name

    def open_pr(self, repo_url: str, branch_name: str, base: str, title: str, body: str) -> str:
        """Open a pull request using the GitHub MCP server."""
        pr_payload = {
            "repo_url": repo_url,
            "branch": branch_name,
            "base": base,
            "title": title,
            "body": body
        }
        response = requests.post(f"{self.mcp_url}/pull-request", json=pr_payload, headers=self.headers)
        response.raise_for_status()
        return response.json().get("pr_url")