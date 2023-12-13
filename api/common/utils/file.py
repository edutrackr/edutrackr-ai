import os
import pathlib


def check_file(base_path, file_path) -> str:
    full_path = os.path.join(base_path, file_path)
    if not os.path.exists(full_path):
        raise ValueError(f"File '{full_path}' does not exist")
    return full_path

def write_file(path, content, binary=True):
    write_mode = "wb" if binary else "w"
    with open(path, write_mode) as f:
        f.write(content)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

def remove_dir_contents(path):
    if os.path.exists(path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

def get_file_extension(file_path):
    """
    Get file extension from file path (e.g. .txt, .png, .jpg, etc.)
    """
    return pathlib.Path(file_path).suffix
