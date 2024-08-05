from typing import TypedDict, Literal

class MetaUrls(TypedDict):
    download_invoice: str

MetaPage = TypedDict('MetaPage', {
    "current_page": int,
    "from": int,
    "last_page": int,
    "per_page": int,
    "to": int,
    "total": int,
})

class Meta(TypedDict):
    test_mode: bool
    page: MetaPage
    period_start: str
    period_end: str
    quantity: int
    interval_unit: Literal["day", "week", "month", "year"]
    interval_quantity: int
    urls: MetaUrls