"""
MCP AI Agent

This package contains the modules responsible for:
- Connecting to MCP servers (GitHub, Jira)
- Loading context (repo files, ticket data)
- Building prompts
- Sending to LLM (Gemini)
- Applying code changes
- Logging and configuration
"""

from agent.base_agent import BaseAgent
from agent.config.settings import settings

__all__ = ["BaseAgent", "settings"]
