from enum import Enum


class StatusCode(Enum):
    SUCCESS = (200, "Success")
    NOT_FOUND = (404, "Not Found")
    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")

    def __init__(self, code: int, description: str):
        self._value_ = code
        self.description = description