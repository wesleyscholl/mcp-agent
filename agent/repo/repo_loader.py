import os

EXCLUDED_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv"}
INCLUDED_EXTENSIONS = {".py", ".js", ".ts", ".json", ".yaml", ".yml"}

def is_valid_file(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext in INCLUDED_EXTENSIONS


def list_code_files(base_path: str = ".", max_files: int = 50) -> list:
    """
    Recursively collects code file paths, filtering by extension and excluding common dirs.
    """
    files = []
    for root, dirs, filenames in os.walk(base_path):
        # Remove excluded dirs in-place to prevent recursion
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for fname in filenames:
            fpath = os.path.join(root, fname)
            if is_valid_file(fpath):
                files.append(fpath)
            if len(files) >= max_files:
                return files
    return files


def extract_file_snippet(file_path: str, max_lines: int = 100) -> str:
    """
    Returns up to `max_lines` of content from the file, used for prompt building.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[:max_lines]
            return "".join(lines)
    except Exception as e:
        return f"# [Error reading {file_path}]: {e}"


def load_repo_context(base_path: str = ".", max_files: int = 50, max_lines_per_file: int = 100) -> list:
    """
    Loads repo files and extracts snippets for LLM context.
    Returns: List of dicts with 'path' and 'snippet'.
    """
    file_paths = list_code_files(base_path, max_files)
    context = []

    for path in file_paths:
        snippet = extract_file_snippet(path, max_lines_per_file)
        relative_path = os.path.relpath(path, base_path)
        context.append({"path": relative_path, "snippet": snippet})

    return context
