from typing import TypeVar, Generic

from pydantic import BaseModel, ConfigDict

from ..utils import Error

T = TypeVar('T')

class FetchResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status_code: int | None = None
    data: T | None = None
    error: Error | None = None