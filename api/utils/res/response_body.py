from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar('T')

class ResponseBody(BaseModel, Generic[T]):
    code: int
    message: str
    body: T
    status: bool