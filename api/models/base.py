from typing import Generic, TypeVar
from pydantic import BaseModel


TData = TypeVar("TData")

class BaseResponse(BaseModel, Generic[TData]):
    success: bool
    message: str | None = None
    data: TData | None = None

class EmptyResponse(BaseResponse[None]):
    pass
