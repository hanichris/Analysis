from typing import Any

from pydantic import BaseModel

class Links(BaseModel):
    about: str | None = None
    type: str | None = None

class Source(BaseModel):
    pointer: str | None = None
    parameter: str | None = None

class JSONAPIError(BaseModel):
    id: str | None = None
    links: Links | None = None
    status: str | None = None
    code: str | None = None
    title: str
    detail: str | None = None
    source: Source | None = None
    meta: dict[str, Any] | None = None


class Error:
    name = "Lemon Squeezy Error"

    def __init__(self, message: str) -> None:
        self.message = message
    
    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, value: str) -> None:
        self._message = value

    @property
    def cause(self) -> str | list[JSONAPIError]:
        return self._cause
    
    @cause.setter
    def cause(self, value: str | list[JSONAPIError]) -> None:
        self._cause = value

    def __repr__(self) -> str:
        return f"{self.name}: {self.message}"
