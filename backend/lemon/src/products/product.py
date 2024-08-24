from ..internal.request import fetch, FetchOptions, FetchResponse
from ..internal.utils import params_to_query_string, include_to_query_string
from .types import GetProductParams, ListProductParams, Product, ListProducts

async def get_product(
        product_id: int | str,
        params: dict = {}
):
    """Retrive the information about the provided product ID.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for the product with the given id.

    Args:
        product_id: The id of the product of interest.
        params: Optional dictionary of parameters.

    Returns:
        Response object with the keys `data`, `error` and `status_code`.

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature.
    """
    options = FetchOptions(
        path=f"/v1/products/{product_id}",
        param=include_to_query_string(
            GetProductParams(**params).include
        )
    )
    return FetchResponse[Product](**await fetch(options)).model_dump()

async def list_products(params: dict = {}):
    """Retrieve a list of products.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for a list of products.

    Args:
        params: Optional set of path parameters.

    Returns:
        Response object with the keys `data`, `error`, and `status_code`.

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature.
    """
    options = FetchOptions(
        path="/v1/products",
        param=params_to_query_string(ListProductParams(**params))
    )
    return FetchResponse[ListProducts](**await fetch(options)).model_dump()