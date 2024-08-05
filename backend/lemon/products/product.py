from ..internal.request import fetch, FetchOptions
from ..internal.utils import params_to_query_string
from .types import GetProductParams, ListProductParams

async def get_product(
        product_id: int | str,
        params: GetProductParams = {} # type: ignore
):
    options = FetchOptions[GetProductParams](
        path=f"/v1/products/{product_id}",
        param=params
    )
    return await fetch(options)

async def list_products(params: ListProductParams):
    options = FetchOptions(
        path="/v1/products",
        param=params_to_query_string(params)
    )
    return await fetch(options)