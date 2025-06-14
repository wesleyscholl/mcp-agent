import os

class RepoContextLoader:
    def __init__(self, repo_path: str, max_file_size: int = 2000):
        self.repo_path = repo_path
        self.max_file_size = max_file_size  # Characters per file to avoid token overflow

    def list_files(self, extensions: list = [".py", ".js", ".ts", ".java"]):
        """Walk through repo and list source code files by extension."""
        code_files = []
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    full_path = os.path.join(root, file)
                    code_files.append(full_path)
        return code_files

    def extract_snippets(self, file_paths: list):
        """Return a dict of filename -> code (trimmed for token limit)."""
        snippets = {}
        for file_path in file_paths:
            try:
                with open(file_path, "r") as f:
                    code = f.read()
                    if len(code) > self.max_file_size:
                        code = code[:self.max_file_size] + "\n# ...truncated..."
                    snippets[file_path] = code
            except Exception as e:
                print(f"Skipping {file_path}: {e}")
        return snippets

    def build_prompt(self, summary: str, description: str, snippets: dict):
        """Build a Gemini-ready prompt from ticket + code snippets."""
        code_blocks = "\n\n".join([f"### {os.path.relpath(fp, self.repo_path)}\n```python\n{code}\n```" 
                                   for fp, code in snippets.items()])
        prompt = f"""
You are an expert software engineer.

### TASK
{summary}

### DETAILS
{description}

### EXISTING CODE CONTEXT
{code_blocks}

Please generate or modify code to solve the issue described above. Write complete and high-quality code.
"""
        return prompt.strip()