import os
import pathlib


def write_file(path, content, binary=True):
    write_mode = "wb" if binary else "w"
    with open(path, write_mode) as f:
        f.write(content)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

def get_file_extension(file_path):
    """
    Get file extension from file path (e.g. .txt, .png, .jpg, etc.)
    """
    return pathlib.Path(file_path).suffix
