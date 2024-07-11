from typing import Callable

from pydantic import BaseModel

from utils import CONFIG_KEY, set_kv, Error

class Config(BaseModel):
    api_key: str | None = None
    on_error: Callable[[Error], None] | None = None

def lemon_squeezy_setup(config: Config) -> Config:
    set_kv(
        CONFIG_KEY,
        {
            "api_key": config.api_key,
            "on_error": config.on_error
        }
    )
    return config
