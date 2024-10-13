import asyncio
import pprint
import os

from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from lemon.src.internal.setup import lemon_squeezy_setup, Config
from lemon.src.checkouts import NewCheckout, create_checkout
from lemon.src.webhooks import list_webhooks, UpdateWebhook, create_webhook
from lemon.src.prices import list_prices, get_price
from lemon.src.subscriptions import list_subscriptions, cancel_subscription, get_subscription, update_subscription

async def bar(error = False):
    if error:
        raise RuntimeError('raising an error')
    return await list_prices()

async def foo():
    plan_task = None
    try:
        async with asyncio.TaskGroup() as tg:
            plan_task = tg.create_task(bar())
            user_task = tg.create_task(bar(error=True))
            price_task = tg.create_task(bar())
    except ExceptionGroup as exc:
        print('One of the tasks failed')
    
    plan = None
    try:
        plan = plan_task.result() if plan_task else plan
    except (Exception, asyncio.CancelledError):
        print('error occurred.')

    return plan


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
            'enabled_variants': [int(variant_id)],
            'redirect_url': f"{os.getenv('PUBLIC_URL')}/dashboard",
            'receipt_button_text': 'Go to Dashboard',
            'receipt_thank_you_note': 'Thank you for signing up to Divergent AG'
        } ,
        "checkout_options": {
            "embed": True,
            "media": True,
            "logo": True,
        },
        "checkout_data": {
            "email": "tita0x00@gmail.com",
            "tax_number": "12345",
            "custom": {
                "user_id": "1234567890",
            },
        },
        "expires_at": None,
        "preview": True,
        "test_mode": True,
    }

    checkout: NewCheckout = {
        'checkout_options': {
            'embed': True,
            'media': False,
            'logo': True,
        },
        'checkout_data': {
            'email': "hanichris71@gmail.com",
            'custom': {
                'user_id': '296a4772026c46ef9a5494b62590a9ae',
            },
        },
        'product_options': {
            'enabled_variants': [int(variant_id)],
            'redirect_url': f"{os.getenv('PUBLIC_URL')}/dashboard",
            'receipt_button_text': 'Go to Dashboard',
            'receipt_thank_you_note': 'Thank you for signing up to Divergent AG'
        },
        'preview': True,
    }
    # val = os.getenv("SECERET_KEY") == os.getenv("LEMONSQUEEZY_WEBHOOK_SECRET")
    # val = asyncio.run(create_webhook(
    #     store_id,
    #     {
    #         'url': 'https://previously-funny-bee.ngrok-free.app/api/webhook',
    #         'secret': cast(str, os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')),
    #         'events': [
    #             'subscription_created',
    #             'subscription_expired',
    #             'subscription_updated',
    #         ],
    #         'test_mode': True
    #     }
    # ))

    # val = asyncio.run(create_checkout(
    #     store_id,
    #     variant_id,
    #     {
    #         'checkout_options': {
    #             'embed': True,
    #             'media': False,
    #             'logo': True,
    #         },
    #         'checkout_data': {
    #             'email': 'albertmbogokuria@gmail.com',
    #             'custom': {
    #                 'user_id': '8652c3435313405b8907b02f4e0c82c8',
    #             },
    #         },
    #         'product_options': {
    #             'enabled_variants': [int(variant_id)],
    #             'redirect_url': f"{os.getenv('PUBLIC_URL')}/dashboard",
    #             'receipt_button_text': 'Go to Dashboard',
    #             'receipt_thank_you_note': 'Thank you for signing up to Divergent AG'
    #         },
    #         'preview': True, # if missing, LEMONSQUEEZY returns a 500 server error.
    #     }
    # ))
    val = asyncio.run(update_subscription(579702, {
        'pause': {
            'mode': 'void',
        }
    }))
    pprint.pprint(val)

if __name__ == "__main__":
    main()