from typing import Any


kv: dict[str, Any] = {}

def get_kv(key: str) -> Any | None:
    """Get the `value` corresponding to the `key`.

    Args:
        key: String type key.

    Returns:
        `Value` corresponding to the `key` passed in. `None`, otherwise.
    """
    return kv.get(key)

def set_kv(key: str, value: Any) -> None:
    """Set the `value` corresponding to the `key`.

    Args:
        key: String type key.
        value: The value to be set.
    """
    kv[key] = value
