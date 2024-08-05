from typing import Literal, TypedDict, Sequence, Iterator, Any, NotRequired

from pydantic import create_model, RootModel

from ..types.response import (
    RelationshipLinks,
    RelationshipKeys,
    Data,
    Params,
)



class Pick[T]:
    keys: Sequence[T]
    def __init__(self, keys: Sequence[T]) -> None:
        Pick.keys = keys
    
    @classmethod
    def pick(cls):
        assert isinstance(cls.keys, list), "Provide the keys as a 'list' or 'tuple'"
        keys_model = create_model(
            'Keys', **{key: (RelationshipLinks, ...) for key in cls.keys}
        ) # type: ignore
        class Keys(RootModel):
            root: keys_model # type: ignore

            def __getitem__(self, item: RelationshipKeys) -> RelationshipLinks:
                return self.root[item]

            def __iter__(self) -> Iterator[RelationshipKeys]:
                return iter(self.root)
        
        return Keys

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

class ProductData(Data[Attributes, Pick[str](["stores", "variants"]).pick()]):
    pass

class GetProductParams(Params[list[Literal['stores', 'variants']], dict[str, Any]]):
    pass

class ListProductParams(Params[list[Literal['stores', 'variants']], StoreId]):
    pass