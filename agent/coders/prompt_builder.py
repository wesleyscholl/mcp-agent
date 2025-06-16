import textwrap
from typing import List, Dict


def build_prompt(ticket: Dict, file_contexts: List[Dict]) -> str:
    """
    Constructs a natural language prompt for the LLM based on the ticket and relevant code.

    :param ticket: dict containing ticket data (e.g. id, title, description)
    :param file_contexts: list of dicts with 'path' and 'snippet' keys
    :return: formatted prompt string
    """
    ticket_block = textwrap.dedent(f"""
        Jira Ticket:
        - ID: {ticket.get("id")}
        - Title: {ticket.get("title")}
        - Description: {ticket.get("description")}
    """)

    file_blocks = "\n\n".join(
        f"### File: {f['path']}\n{f['snippet']}" for f in file_contexts
    )

    prompt = f"""
You are an AI code assistant. Use the following context to generate or modify Python code.

{ticket_block}

Relevant Code Files:
{file_blocks}

Instructions:
- Focus only on the logic related to the ticket
- Use existing patterns and styles from the files
- If new files are needed, include full path and content

Respond with the updated code changes.
"""

    return prompt.strip()
