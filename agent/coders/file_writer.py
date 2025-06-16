import os


def write_code_file(path: str, content: str, base_dir: str = "."):
    """
    Write or overwrite a file with the given content.

    :param path: file path relative to base_dir
    :param content: full content to write
    :param base_dir: base directory to resolve relative paths
    """
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[file_writer] Wrote to {full_path}")
