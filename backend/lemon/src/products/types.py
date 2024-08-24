from typing import Literal, TypedDict, Any, NotRequired, ClassVar

from ..types.response import (
    RelationshipKeys,
    Data,
    Params,
    Pick
)

class Attributes(TypedDict):
    store_id: int
    name: str
    slug: str
    description: str
    status: Literal["published", "draft"]
    status_formatted: str
    thumb_url: str
    large_thumb_url: str
    price: int
    price_formatted: str
    from_price: int | None
    from_price_formatted: str | None
    to_price_formatted: str | None
    to_price: int | None
    pay_what_you_want: bool
    buy_now_url: str
    created_at: str
    updated_at: str
    test_mode: bool

class StoreId(TypedDict):
    store_id: NotRequired[int | str]

class ProductData(
    Data[Attributes, Pick[RelationshipKeys](keys=["store", "variants"]).pick()]
):
    pass

class GetProductParams(Params[list[Literal['store', 'variants']], dict[str, Any]]):
    filter: ClassVar
    page: ClassVar

class ListProductParams(Params[list[Literal['store', 'variants']], StoreId]):
    pass