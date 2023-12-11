from fastapi import status

class AppException(Exception):
    def __init__(self, description: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.description = description
        self.status_code = status_code
