"""
OS utilities.
"""

import os


def get_env(key, default=None):
    value = os.getenv(key)
    if value is None and default is None:
        raise ValueError(f"Environment variable '{key}' not set")
    return value or default

def remove_env(key):
    if key in os.environ:
        os.environ.pop(key)

def get_path(base_path, file_path, create_dir=False, ignore_exists=False):
    full_path = os.path.join(base_path, file_path)
    if create_dir and not os.path.exists(base_path):
        os.makedirs(base_path)
    if not ignore_exists and not os.path.exists(full_path):
        raise ValueError(f"Path '{full_path}' does not exist")
    return full_path

def gen_key():
    return str(os.urandom(16).hex())

if __name__ == "__main__":
    print(gen_key())
