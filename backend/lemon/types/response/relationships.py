from collections.abc import Iterator
from typing import Literal, TypedDict

from pydantic import RootModel, BaseModel


type Types = Literal[
    "stores",
    "customers",
    "products",
    "variants",
    "prices",
    "files",
    "orders",
    "order-items",
    "subscriptions",
    "subscription-invoices",
    "subscription-items",
    "usage-records",
    "discounts",
    "discount-redemptions",
    "license-keys",
    "license-key-instances",
    "checkouts",
    "webhooks",
]

type RelationshipKeys = Literal[
    "store",
    "product",
    "variant",
    "customer",
    "order",
    "order-item",
    "subscription",
    "price",
    "price-model",
    "subscription-item",
    "discount",
    "license-key",
    Types
]

class Links(TypedDict):
    related: str
    self: str

class Data(TypedDict):
    id: str
    type: Types

class RelationshipLinks(BaseModel, revalidate_instances='always'):
    link: Links
    data: list[Data] | None = None


class Relationship(RootModel):
    root: dict[RelationshipKeys, RelationshipLinks]

    def __getitem__(self, item: RelationshipKeys) -> RelationshipLinks:
        return self.root[item]

    def __iter__(self) -> Iterator[RelationshipKeys]:
        return iter(self.root)
