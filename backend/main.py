import asyncio
import pprint
import os

from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from lemon.src.internal.setup import lemon_squeezy_setup, Config
from lemon.src.checkouts import NewCheckout
from lemon.src.webhooks import list_webhooks, UpdateWebhook

def main():
    BASE_DIR = Path(__file__).resolve().parent

    load_dotenv(os.path.join(BASE_DIR, '.env'))

    lemon_squeezy_setup(Config(
        api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
    ))

    product_id = cast(str, os.getenv("LEMONSQUEEZY_PRODUCT_ID"))
    price_id = cast(str, os.getenv("LEMONSQUEEZY_PRICE_ID"))
    variant_id = cast(str, os.getenv("LEMONSQUEEZY_VARIANT_ID"))
    store_id = cast(str, os.getenv("LEMONSQUEEZY_STORE_ID"))
    sub_id = cast(str, os.getenv("LEMONSQUEEZY_USER_SUB_SUBSCRIPTION_ID"))
    webhook_id = cast(str, os.getenv("LEMONSQUEEZY_WEBHOOK_ID"))

    new_checkout: NewCheckout = {
        "product_options": {            
            "name": "New Checkout Test",
            "description": "a new checkout test",
            "media": ["https://google.com"],
            "redirect_url": "https://google.com",
            "receipt_button_text": "Text Receipt",
            "receipt_link_url": "https://lemonsqueezy.com",
            "receipt_thank_you_note": "Thanks to lemonsqueezy",
            "enabled_variants": [int(variant_id)],
            "confirmation_title": "Thank you for your support",
            "confirmation_message": "Thank you for subscribing and have a great day",
            "confirmation_button_text": "View Order",
        },
        "checkout_options": {
            "embed": True,
            "media": True,
            "logo": True,
            "desc": True,
            "dark": True,
            "skip_trial": True,
            "discount": False,
            "button_color": "#ccc",
            "subscription_preview": True,
        },
        "checkout_data": {
            "email": "tita0x00@gmail.com",
            "name": "Lemon Squeezy Test",
            "billing_address": {                
                "country": "US",
            },
            "tax_number": "12345",
            # discountCode: 'Q3MJI5MG',
            "custom": {
                "user_id": "1234567890",
                "user_name": "Mrs.A",
                "nick_name": "AAA",
            },
            "variant_quantities": [],
        },
        "expires_at": None,
        "preview": True,
        "test_mode": True,
    }
    val = asyncio.run(list_webhooks({
            "filter": {
                "store_id": store_id
            }
        }))
    pprint.pprint(val)

if __name__ == "__main__":
    main()