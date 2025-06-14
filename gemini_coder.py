import os
import google.generativeai as genai

class GeminiCoder:
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_code(self, prompt: str) -> str:
        """Send prompt to Gemini and return generated code (as text)."""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""

    def write_code_to_file(self, output_code: str, repo_path: str, relative_path: str = "generated_code.py"):
        """Write generated code into a file within the repo."""
        full_path = os.path.join(repo_path, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(output_code)
        print(f"✅ Code written to {full_path}")
        return full_path