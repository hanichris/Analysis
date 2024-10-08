import functools
import hashlib
import os
import random
import sys

from typing import Callable, Any
from django.core.cache import cache


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
    def decorator_func(f: Callable):
        @functools.wraps(f)
        def wrapper_func(*args, **kwargs):
            cache_key = generate_key(f, *args, *kwargs)
            if prefix:
                cache_key = f'{prefix}_{cache_key}'
            print(f"Cache key: {cache_key}")
            # On cache hit: return the cachced result.
            if cached_result := cache.get(cache_key):
                print('\033[34;1mINFO: Cache hit.\033[0m')
                return cached_result
            
            # On cache miss: compute the result, cache it and return.
            if result := f(*args, *kwargs):
                print('\033[34;1mINFO: Cache miss.\033[0m')
                cache.set(cache_key, result, timeout=timeout)
            else:
                print(
                    '\033[33;1mWARNING: `None` result is not cached.\033[0m',
                    file=sys.stderr
                )
            return result
        return wrapper_func
    return decorator_func

@cache_results(timeout=60)
def foo(entries: list):
    return sorted(entries)


def delete_key(f: Callable):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        cache_key = generate_key(f, *args, *kwargs)
        print(f"Deleteing cache key {cache_key} entry")
        is_successful = cache.delete(cache_key)
        if is_successful:
            print(f"Successfully deleted the object with cache key {cache_key}")
        else:
            print(f"Failed to delete the object with the cache key {cache_key}")
        return is_successful
    return wrapper


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    entries = [random.randint(1, 10) for _ in range(20)]

    sorted_entries = foo(entries)
    print(sorted_entries)
    sorted_entries = foo(entries)
    print(sorted_entries)
    sorted_entries = foo(entries)
    print(sorted_entries)
    is_successful = delete_key(foo)(entries)
    print(f"{is_successful = }")
    sorted_entries = foo(entries)
    print(sorted_entries)