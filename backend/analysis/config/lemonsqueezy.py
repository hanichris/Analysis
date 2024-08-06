import os

from lemon.src.internal.setup import Config, lemon_squeezy_setup
from lemon.src.internal.utils import Error

def err_fn(error: Error):
    """Raises a runtime exception with the provided `Error` message.

    Args:
        error: The error that has occurred.
    
    Raises:
        RuntimeError: When an unexpected error occurs during execution.
    """
    raise RuntimeError(f"Lemon Squeezy API error: {error.message}")

def configure_lemonsqueezy():
    """Sets up lemon squeezy for use.

    Ensures the required environment variables are set. A `ValueError`
    exception is raised if any of the environment variables is missing.
    A `RuntimeError` is raise if there is error setting up lemon
    squeezy.

    Raises:
        ValueError: If any of the required environment variables is missing.
        RuntimeError: If an error occurred while setting up lemon squeezy.
    """

    required_vars = (
        "LEMONSQUEEZY_API_KEY",
        "LEMONSQUEEZY_STORE_ID",
        "LEMONSQUEEZY_WEBHOOK_SECRET",
    )

    missing_vars = [x for x in required_vars if os.getenv(x) is None]
    if missing_vars:
        raise ValueError(
            'Missing required LEMONSQUEEZY env variables: '
            f"`{', '.join(missing_vars)}`. Please, set them in your .env file."
        )
    
    lemon_squeezy_setup(Config(
        api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        on_error= err_fn
    ))
