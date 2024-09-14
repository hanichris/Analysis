import functools
import hashlib
import os
import sys

from typing import Any, Callable, Coroutine, TypedDict

from django.core.cache import cache
from pydantic import BaseModel, ValidationError

class CustomData(TypedDict):
    user_id: str

class Meta(TypedDict):
    event_name: str
    custom_data: CustomData

class EventMetaAttribute(BaseModel):
    meta: Meta

class EventDataAttribute(BaseModel):
    data: dict

def webhook_has_meta(obj):
    valid = True
    try:
        EventMetaAttribute.model_validate(obj)
    except ValidationError:
        valid = False
    return valid

def webhook_has_data(obj):
    valid = True
    try:
        EventDataAttribute.model_validate(obj)
    except ValidationError:
        valid = False
    return valid

def generate_namespace(f: Callable[..., Any]):
    """Generates a unique namespace for the callable object.

    Utilises the module name in which the callable object is defined as well as
    its qualifying name to generate a unique namespace for it.
    Args:
        f: A callable object.
    Returns:
        str: The namespace of the callable object.
    """
    return f'{f.__module__}.{f.__qualname__}'

def hash_data(s: bytes | str, algo: str = 'md5'):
    """Compute a fixed-length hash of the given data.

    Generates a compact and unique representation of the data structure. It
    is particularly useful when it comes to larger data structures.
    Args:
        s: bytes-like object or a string literal.
        algo: the hashing algorithm to use.
    Returns:
        str: The fixed length hash value containing only hexadecimal digits.
    """
    if isinstance(s, str):
        s = s.encode()
    return hashlib.new(algo, s).hexdigest()

def generate_key(f: Callable, *args, **kwargs):
    """Generate a unique key for the callable object to be used in a cache store.
    
    Generates a key by incorporating the callable object's namespace and hashed
    arguments. The key then serves to retrieve the results of callable object from
    a cache store and storing the said results within the cache.
    Args:
        f: callable object.
    Returns:
        str: the callable object's unique key.
    """
    key = generate_namespace(f)
    arg_hash = hash_data(f'{args}{kwargs}') if args or kwargs else None
    if arg_hash:
        key = f'{key}.{arg_hash}'
    return key


def cache_results(
    timeout: int | None = None, prefix: str | None = os.getenv('ENV_NAME')
) -> Any:
    """Decorator to cache the results of a callable object.
    
    Employs the callable objects parameters as part of the key to access the cache
    store. Maintains a clean and efficient caching strategy, especially for
    frequently used callable objects with dynamic arguments.
    Args:
        timeout: Optional. The duration (in seconds) to keep the results in the
                the cache. If None, the results are cached indefinitely. Default
                is None.
        prefix: Optional. The prefix to use for the cache key. Useful for
                namespacing aspects. Defaults to the value of the `ENV_NAME`
                environment variable if it is available.
    Returns:
        Any: The cached results of the callable object if available. Otherwise, the
        results are computed, cached and returned.
    """
    def decorator_func(f: Callable[..., Coroutine]):
        @functools.wraps(f)
        async def wrapper_func(*args, **kwargs):
            cache_key = generate_key(f, *args, *kwargs)
            if prefix:
                cache_key = f'{prefix}_{cache_key}'
            # On cache hit: return the cachced result.
            if cached_result := await cache.aget(cache_key):
                print('\033[34;1mINFO: Cache hit.\033[0m')
                return cached_result
            
            # On cache miss: compute the result, cache it and return.
            if result := await f(*args, *kwargs):
                print('\033[34;1mINFO: Cache miss.\033[0m')
                await cache.aset(cache_key, result, timeout=timeout)
            else:
                print(
                    '\033[33;1mWARNING: `None` result is not cached.\033[0m',
                    file=sys.stderr
                )
            return result
        return wrapper_func
    return decorator_func

def del_cache_key(f: Callable, prefix: str | None = os.getenv('ENV_NAME')):
    """Deletes the object associated with the provided key from the cache.
    
    Args:
        f: The callable object whose results are to be removed from the cache.
    Returns:
        f: wrapper function that performs the eviction operation.
    """
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        cache_key = generate_key(f, *args, *kwargs)
        if prefix:
            cache_key = f'{prefix}_{cache_key}'
        print(f"Deleteing cache key {cache_key} entry")
        await cache.adelete_many([cache_key])
        is_successful = False
        if await cache.aget(cache_key):
            print(f"Failed to delete the object with the cache key {cache_key}")
        else:
            print(f"Successfully deleted the object with cache key {cache_key}")
            is_successful = True
        return is_successful
    return wrapper
