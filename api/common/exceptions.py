class AppException(Exception):
    def __init__(self, description: str, status_code: int = 500):
        self.description = description
        self.status_code = status_code
