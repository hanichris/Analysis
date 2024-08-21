from ..internal.request import fetch, FetchOptions
from ..internal.utils import params_to_query_string, include_to_query_string

from .types import GetPriceParams, ListPriceParams

async def get_price(
        price_id: int | str,
        params: dict = {}
):
    """Retrive the information about the provided price ID.

    Makes a `GET` request with an optional set of path parameters
    to the lemonSqueezy API for the price with the given id.

    Args:
        price_id: The id of the price of interest.
        params: Optional dictionary of parameters.

    Returns:
        Response object with the keys `data`, `error`
        and `status_code`.

    Raises:
        ValidationError: If the parameters passed do not match
        the required signature.
    """
    options = FetchOptions(
        path=f"/v1/prices/{price_id}",
        param=include_to_query_string(
            GetPriceParams(**params).include
        )
    )
    return await fetch(options)

async def list_prices(params: dict = {}):
    """Retrieve a list of prices.

    Makes a `GET` request with an optional set of path parameters
    to the lemonSqueezy API for a list of prices.

    Args:
        params: Optional set of path parameters.

    Returns:
        Response object with the keys `data`, `error`, and
        `status_code`.

    Raises:
        ValidationError: If the parameters passed do not match
        the required signature.
    """
    options = FetchOptions(
        path="/v1/prices",
        param=params_to_query_string(ListPriceParams(**params))
    )
    return await fetch(options)