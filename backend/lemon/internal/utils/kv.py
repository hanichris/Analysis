from typing import Any


kv: dict[str, Any] = {}

def get_kv(key: str) -> Any | None:
    return kv.get(key)

def set_kv(key: str, value: Any) -> None:
    kv[key] = value
