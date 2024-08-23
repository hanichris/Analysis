from collections.abc import Iterator, Sequence
from typing import Literal, Generic, TypedDict, TypeVar

from pydantic import BaseModel, create_model, ConfigDict, RootModel


T = TypeVar('T')

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

    def __getitem__(self, item) -> Links | list[Data] | None:
        return getattr(self, item)


class Relationship(RootModel):
    root: dict[RelationshipKeys, RelationshipLinks]

    def __getitem__(self, item: RelationshipKeys) -> RelationshipLinks:
        return self.root[item]

    def __iter__(self) -> Iterator[RelationshipKeys]:
        return iter(self.root)

class Pick(BaseModel, Generic[T]):
    keys: Sequence[T]

    def pick(self):
        config = {
            'extra': 'forbid',
            'validate_assignment': True
        }
        keys_model = create_model(
            'Keys',
            __config__=ConfigDict(**config),
            **{key: (RelationshipLinks, ...) for key in self.keys}
        ) # type: ignore
        class Keys(RootModel):
            root: keys_model # type: ignore

            def __getitem__(self, item) -> RelationshipLinks:
                return getattr(self.root, item)

            def __iter__(self) -> Iterator[T]:
                return iter(self.root)
        
        return Keys


if __name__ == "__main__":

    Model = Pick[RelationshipKeys](keys=['store', 'variant']).pick()
    
    data = {
        'store': {
            'link': {
                'related': '',
                'self': '',
            },
            'data': [
                {
                    'id': '',
                    'type': 'discounts',
                }
            ]
        },
        'variant': {
            'link': {
                'related': '',
                'self': '',
            }
        },
    }
    valid = Model(data)
    