import sys
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel

from utils import get_kv, CONFIG_KEY, API_BASE_URL, Error, JSONAPIError


class HTTPVerbEnum(str, Enum):
    get     = "GET"
    post    = "POST"
    delete  = "DELETE"
    put     = "PUT"
    patch   = "PATCH"


class FetchOptions(BaseModel):
    path: str
    method: HTTPVerbEnum | None = None
    param: dict[str, Any] | None = None
    body: dict[str, Any] | None = None


def create_lemon_error(
        message: str,
        cause: str | list[JSONAPIError] = "unknown"
) -> Error:
    error = Error(message)
    error.cause = cause
    return error


async def fetch(options: FetchOptions, requiresApi = True):
    response = {
        "status_code": None,
        "data": None,
        "error": None | Error,
    }

    config: dict | None = get_kv(CONFIG_KEY)
    if config is None or (key := config.get("api_key") is None):
        response["error"] = create_lemon_error(
            "Please provide your Lemon Squeezy API key. Create a new API key at "
            "`https://app.lemonsqueezy.com/settings/api`",
            "Missing API key"
        )
        print(response["error"], file=sys.stderr)
        return response
    
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
    }

    if requiresApi:
        headers["Authorization"] = f"Bearer {config["api_key"]}"

    data = options.body if options.method in {"PATCH", "POST"} else None
    async with httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers=headers,
        params=options.param
    ) as client:
        match options.method:
            case "GET":
                res = await client.get(options.path)
            case "POST":
                res = await client.post(options.path, json=data)
            case "DELETE":
                res = await client.delete(options.path)
            case "PATCH":
                res = await client.patch(options.path, json=data)
            case _:
                print("Unrecognised HTTP verb", file=sys.stderr)
                response["error"] = create_lemon_error(
                    f"Unrecognised HTTP verb: {options.method}",
                    "unknown HTTP verb"
                )
                return response
    
    if(res.status_code == httpx.codes.OK):
        response["status_code"] = res.status_code
        response["data"] = res.json()
    else:
        _data: dict[str, Any] = res.json()
        _error = \
        _data.get("errors") or \
        _data.get("error") or \
        _data.get("message") or \
        "unknown cause"

        response["status_code"] = res.status_code
        response["data"] = _data
        response["error"] = create_lemon_error(res.text, _error)

    return response