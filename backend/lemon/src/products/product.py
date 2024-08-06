from ..internal.request import fetch, FetchOptions
from ..internal.utils import params_to_query_string, include_to_query_string
from .types import GetProductParams, ListProductParams

async def get_product(
        product_id: int | str,
        params: dict = {}
):
    options = FetchOptions(
        path=f"/v1/products/{product_id}",
        param=include_to_query_string(
            GetProductParams(**params).include
        )
    )
    return await fetch(options)

async def list_products(params: ListProductParams):
    options = FetchOptions(
        path="/v1/products",
        param=params_to_query_string(params)
    )
    return await fetch(options)