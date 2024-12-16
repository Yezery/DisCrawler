from pydantic import BaseModel
from typing import Any, Dict, Generic, TypeVar, List, Optional, Union

from service.utils.StatusCode import StatusCode

# 定义类型变量
T = TypeVar('T')

# 封装结果类
class Result(BaseModel, Generic[T]):
    code: int
    message: str
    data: Any

    @classmethod
    def success(cls, data = None) -> "Result":
        return cls(code=StatusCode.SUCCESS.value, message=StatusCode.SUCCESS.description, data=data)

    @classmethod
    def not_found(cls, message: str = "Resource not found") -> "Result":
        return cls(code=StatusCode.NOT_FOUND.value, message=message)

    @classmethod
    def bad_request(cls, message: str = "Bad request") -> "Result":
        return cls(code=StatusCode.BAD_REQUEST.value, message=message)

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized access") -> "Result":
        return cls(code=StatusCode.UNAUTHORIZED.value, message=message)

    @classmethod
    def forbidden(cls, message: str = "Access forbidden") -> "Result":
        return cls(code=StatusCode.FORBIDDEN.value, message=message)

    @classmethod
    def internal_server_error(cls, message: str = "An internal error occurred") -> "Result":
        return cls(code=StatusCode.INTERNAL_SERVER_ERROR.value, message=message)
    
