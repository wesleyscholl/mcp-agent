import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

class Settings:
    # MCP endpoints
    GITHUB_MCP_URL = os.getenv("GITHUB_MCP_URL")
    JIRA_MCP_URL = os.getenv("JIRA_MCP_URL")

    # Authentication
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    JIRA_TOKEN = os.getenv("JIRA_TOKEN")

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # PostgreSQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "mcp_context")
    DB_USER = os.getenv("DB_USER", "mcp_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Agent behavior
    MAX_FILES = int(os.getenv("MAX_FILES", 50))
    MAX_LINES_PER_FILE = int(os.getenv("MAX_LINES_PER_FILE", 2000))


# Create a singleton-style config object
settings = Settings()