from agent.config.settings import settings
from agent.context.context_loader import load_context
from agent.context.context_store import save_context
from agent.coders.prompt_builder import build_prompt
from agent.coders.gemini_coder import generate_code
from agent.coders.file_writer import write_code_file
from agent.utils.logging_utils import get_logger

logger = get_logger(__name__)


class BaseAgent:
    """
    Core agent that orchestrates the workflow:
    1. Loads context from MCP (GitHub/Jira) and repo
    2. Builds a prompt
    3. Sends prompt to LLM (Gemini)
    4. Writes output code
    5. Saves context to PostgreSQL
    """

    def __init__(self, ticket_id: str):
        self.ticket_id = ticket_id
        self.context = None
        self.generated_files = []

    def run(self):
        logger.info(f"Starting agent for ticket: {self.ticket_id}")

        # 1. Load context from Jira + GitHub + repo
        self.context = load_context(ticket_id=self.ticket_id)
        logger.debug(f"Loaded context: {self.context.keys()}")

        # 2. Build LLM prompt
        prompt = build_prompt(
            ticket=self.context["ticket"],
            file_contexts=self.context["files"]
        )
        logger.debug("Prompt built successfully")

        # 3. Send prompt to Gemini
        llm_response = generate_code(prompt)
        logger.debug("Received response from Gemini")

        # 4. Apply file changes
        for file in llm_response.get("files", []):
            path = file["path"]
            content = file["content"]
            write_code_file(path, content)
            self.generated_files.append(path)

        # 5. Save result to context store
        save_context(
            ticket_id=self.ticket_id,
            changes=self.generated_files,
            notes=llm_response.get("notes", "")
        )

        logger.info(f"Agent finished. Updated files: {self.generated_files}")
