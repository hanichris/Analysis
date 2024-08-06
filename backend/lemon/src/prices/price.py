from ..internal.request import fetch, FetchOptions
from ..internal.utils import params_to_query_string, include_to_query_string

async def get_price(
        price_id: int | str,
        params = {}
):
    options = FetchOptions(
        path=f"/v1/prices/{price_id}",
        param=params
    )
    return await fetch(options)

async def list_prices(params = {}):
    options = FetchOptions(
        path="/v1/prices",
        param=params_to_query_string(params)
    )
    return await fetch(options)