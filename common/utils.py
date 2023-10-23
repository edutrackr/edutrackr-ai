import os


def get_env(key, default=None):
    value = os.getenv(key)
    if value is None and default is None:
        raise ValueError(f"Environment variable '{key}' not set")
    return value or default

def get_path(base_path, file_path):
    full_path = os.path.join(base_path, file_path)
    if not os.path.exists(full_path):
        raise ValueError(f"Path '{full_path}' does not exist")
    return full_path