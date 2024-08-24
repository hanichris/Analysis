from typing import Literal, TypedDict, ClassVar, Any

from pydantic import Field

from ..types import ISO3166Alpha2CountryCode, ISO4217CurrencyCode
from ..types.response import (
    Data,
    Params,
    RelationshipKeys,
    Pick
)


class Variant(TypedDict):
    variant_id: int
    quantity: int

class BillingAddress(TypedDict):
    country: ISO3166Alpha2CountryCode
    zip: str

class OptionalBillingAddress(TypedDict, total=False):
    country: ISO3166Alpha2CountryCode
    zip: str

class ProductOptions(TypedDict):
    name: str
    description: str
    media: list[str]
    redirect_url: str
    receipt_button_text: str
    receipt_link_url: str
    receipt_thank_you_note: str
    enabled_variants: list[int]
    confirmation_title: str
    confirmation_message: str
    confirmation_button_text: str

class CheckoutOptions(TypedDict):
    embed: bool
    media: bool
    logo: bool
    desc: bool
    discount: bool
    skip_trial: bool
    quantity: int
    dark: bool
    subscription_preview: bool
    button_color: str

class Preview(TypedDict):
    currency: ISO4217CurrencyCode
    currency_rate: int
    subtotal: int
    discount_total: int
    tax: int
    setup_fee_usd: int
    setup_fee: int
    total: int
    subtotal_usd: int
    discount_total_usd: int
    tax_usd: int
    total_usd: int
    subtotal_formatted: str
    discount_total_formatted: str
    setup_fee_formatted: str
    tax_formatted: str
    total_formatted: str

class CheckoutData(TypedDict):
    email: str
    name: str
    billing_address: BillingAddress
    tax_number: str
    discount_code: str
    custom: list | dict
    # An array of variant IDs to enable for this checkout. If this is empty, all variants will be enabled.
    variant_quantities: list[int]


class Attributes(TypedDict):
    store_id: int
    variant_id: int
    custom_price: None | int
    product_options: ProductOptions
    checkout_options: CheckoutOptions
    checkout_data: CheckoutData
    preview: Preview
    expires_at: None | str
    created_at: str
    updated_at: str
    test_mode: bool
    url: str

class OptionalProductOptions(TypedDict, total=False):
    name: str
    description: str
    media: list[str]
    redirect_url: str
    receipt_button_text: str
    receipt_link_url: str
    receipt_thank_you_note: str
    enabled_variants: list[int]
    confirmation_title: str
    confirmation_message: str
    confirmation_button_text: str

class OptionalCheckoutOptions(TypedDict, total=False):
    embed: bool
    media: bool
    logo: bool
    desc: bool
    discount: bool
    skip_trial: bool
    quantity: int
    dark: bool
    subscription_preview: bool
    button_color: str

class OptionalCheckoutData(TypedDict, total=False):
    email: str
    name: str
    billing_address: OptionalBillingAddress
    tax_number: str
    discount_code: str
    custom: list | dict
    variant_quantities: list[Variant]

class NewCheckout(TypedDict, total=False):
    custom_price: int
    product_options: OptionalProductOptions
    checkout_options: OptionalCheckoutOptions
    checkout_data: OptionalCheckoutData
    preview: bool
    test_mode: bool
    expires_at: None | str

class IDS(TypedDict, total=False):
    store_id: int | str
    variant_id: int | str

class CheckoutResponseData(
    Data[Attributes, Pick[RelationshipKeys](keys=['store', 'variant']).pick]
):
    pass

class GetCheckoutParams(Params[list[Literal['store', 'variant']], dict[str, Any]]):
    filter: ClassVar
    page: ClassVar

class ListCheckoutParams(Params[list[Literal['store', 'variant']], IDS]):
    pass