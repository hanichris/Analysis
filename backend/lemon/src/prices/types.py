from typing import Any, Sequence, TypedDict, NotRequired, Literal, Iterator

from pydantic import create_model, RootModel

from ..types.response import (
    Data,
    Params,
    RelationshipKeys,
    RelationshipLinks,
)

type Category = Literal["one_time", "subscription", "lead_magnet", "pwyw"]
type Scheme = Literal["standard", "package", "graduated", "volume"]
type UsageAggregation = Literal["sum", "last_during_period", "last_ever", "max"]
type TaxCode = Literal["eservice", "ebook", "saas"]


class Pick[T]:
    keys: Sequence[T]
    def __init__(self, keys: Sequence[T]) -> None:
        Pick.keys = keys
    
    @classmethod
    def pick(cls):
        assert isinstance(cls.keys, list), "Provide the keys as a 'list'"
        keys_model = create_model(
            'Keys', **{key: (RelationshipLinks, ...) for key in cls.keys}
        ) # type: ignore
        class Keys(RootModel):
            root: keys_model # type: ignore

            def __getitem__(self, item: T) -> RelationshipLinks:
                return self.root[item]

            def __iter__(self) -> Iterator[T]:
                return iter(self.root)
        
        return Keys

class Tier(TypedDict):
    last_unit: str | int
    unit_price: int
    unit_price_decimal: str | None
    fixed_fee: NotRequired[int]

class Attributes(TypedDict):
    variant_id: int
    category: Category
    scheme: Scheme
    usage_aggregation: UsageAggregation | None
    unit_price: int
    unit_price_decimal: str | None
    setup_fee_enabled: bool | None
    setup_fee: int | None
    package_size: int
    tiers: list[Tier] | None
    renewal_interval_unit: Literal["day", "week", "month", "year"] | None
    renewal_interval_quantity: int | None
    trial_interval_unit: Literal["day", "week", "month", "year"] | None
    trial_interval_quantity: int | None
    min_price: int | None
    suggested_price: None
    tax_code: TaxCode
    created_at: str
    updated_at: str


class VariantId(TypedDict):
    variant_id: NotRequired[int | str]

class PriceData(Data[Attributes, Pick[RelationshipKeys](["stores", "variants"]).pick()]):
    pass

class GetPriceParams(Params[list[Literal['stores', 'variants']], dict[str, Any]]):
    pass

class ListPriceParams(Params[list[Literal['stores', 'variants']], VariantId]):
    pass