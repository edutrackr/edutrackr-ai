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

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def join_path(*args) -> str:
    return os.path.join(*args)

def path_exists(path) -> bool:
    return os.path.exists(path)
