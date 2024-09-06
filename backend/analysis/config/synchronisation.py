import asyncio
import os

from typing import cast

from analysis.config import configure_lemonsqueezy
from analysis.models import Plan, User
from lemon.src.products import list_products, get_product
from lemon.src.prices import list_prices
from lemon.src.checkouts import create_checkout
from lemon.src.webhooks import create_webhook, list_webhooks, Webhook

async def sync_plans() -> list[Plan] | None:
    """Synchronises the product variants from Lemon Squeezy with the database.

    Only synchronises the `subscription` variants. If there were variants
    obtained from Lemon Squeezy, then they are made available to the caller.

    Returns:
        list[Plan] | None. The saved plan objects if there were any variants
        obtained from Lemon Squeezy. Otherwise, None.
    """
    configure_lemonsqueezy()

    products = await list_products({
        "filter": {
            "store_id": os.getenv("LEMONSQUEEZY_STORE_ID"),
        },
        "include": ["variants"],
    })

    all_variants: list | None = cast(
        list | None,
        products['data'].get('included')
    )
    if all_variants:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    get_variant_details(
                        variant
                    )
                )
                for variant in all_variants if not (
                    variant['attributes']['status'] == 'draft' or (
                        len(all_variants) != 1 and 
                        variant['attributes']['status'] == 'pending'
                    )
                )
            ]
        response = [result[-1] for result in map(lambda x: x.result(), tasks) if result[0]]
        return await save_variants(response)

async def get_variant_details(
        variant: dict
) -> tuple[bool, dict]:
    """Fetches the information regarding the product name and variant price.

    Makes a `GET` request to retrieve the pricing of the variant and the
    name of the product of which it is a variant of. This information is
    used to build up a variant object.

    Args:
        variant: The product variant whose information is being requested.

    Raises:
        ValidationError. If the information is not in the necessary schema.

    Returns:
        tuple. Details regarding the variant.
    """
    product_name = ''
    async with asyncio.TaskGroup() as tg:
        task_1 = tg.create_task(get_product(
            variant['attributes']['product_id']
        ))
        task_2 = tg.create_task(list_prices({
            "filter": {
                "variant_id": variant['id'],
            },
        }))
    
    product, variant_price = task_1.result(), task_2.result()

    if product_d := cast(dict | None, product.get('data')):
        product_name = product_d['data']['attributes']['name'] or product_name
    
    current_price_obj = price_d['data'][0] if (
        price_d := cast(dict | None, variant_price.get('data'))
    ) else {}

    variant_obj = {
        'name': variant['attributes']['name'],
        'description': variant['attributes']['description'],
        'product_id': variant['attributes']['product_id'],
        'product_name': product_name,
        'variant_id': int(variant['id']),
        'sort': variant['attributes']['sort']
    }
    is_subscription = False
    if current_price_obj:
        variant_obj['interval'] = current_price_obj['attributes']['renewal_interval_unit']
        variant_obj['interval_count'] = current_price_obj['attributes']['renewal_interval_quantity']
        variant_obj['trial_interval'] = current_price_obj['attributes']['trial_interval_unit']
        variant_obj['trial_interval_count'] = current_price_obj['attributes']['trial_interval_quantity']

        is_usage_based = current_price_obj[
            'attributes'
        ]['usage_aggregation'] != None

        variant_obj['is_usage_based'] = is_usage_based

        price = current_price_obj['attributes']['unit_price_decimal'] if (
        is_usage_based) else current_price_obj['attributes']['unit_price']

        price_str = str(price) if price is not None else ''
        variant_obj['price'] = price_str

        is_subscription: bool = (current_price_obj['attributes']['category'] == 'subscription') or is_subscription
        
    return is_subscription, variant_obj

async def save_variants(data: list[dict]) -> list[Plan]:
    """Saves the information regarding the retrieved variants into the database.

    Args:
        data: a list of objects holding information about each variant.
    
    Returns:
        list[Plan]: The variants stored into the database.
    """
    for info in data:
        print(f"Prepping to sync variant {info['name']} with the database...")

    plans = [Plan(**info) for info in data]
    saved_plans =  await Plan.objects.abulk_create(
        plans,
        update_conflicts=True, # type: ignore
        update_fields=[
            'product_id',
            'product_name',
            'name',
            'description',
            'price',
            'is_usage_based',
            'interval',
            'interval_count',
            'trial_interval',
            'trial_interval_count',
            'sort',
        ],
        unique_fields=['variant_id']
    )

    for plan in saved_plans:
        print(f"{plan.name} synced with the database...")
    return saved_plans


async def get_checkout_url(variant_id: int, user: User, embed: bool = True) -> str:
    """Retrieve a checkout url for a given variant.

    Generates a checkout on Lemon Squeezy for a particular variant for a given user
    and retrieves the url from that operation.

    Args:
        variant_id: The id of the variant of interest.
        user: The signed in user.
        embed: whether to generate an overlay for the url or not.

    Returns:
        str: The checkout url.
    """
    configure_lemonsqueezy()

    response = await create_checkout(
        cast(str, os.getenv("LEMONSQUEEZY_STORE_ID")),
        variant_id,
        {
            'checkout_options': {
                'embed': embed,
                'media': False,
                'logo': True,
            },
            'checkout_data': {
                'email': user.email,
                'custom': {
                    'user_id': user.id.hex,
                },
            },
            'product_options': {
                'enabled_variants': [variant_id],
                'redirect_url': f"{os.getenv('PUBLIC_URL')}/dashboard",
                'receipt_button_text': 'Go to Dashboard',
                'receipt_thank_you_note': 'Thank you for signing up to Divergent AG'
            },
            'preview': True, # if missing, LEMONSQUEEZY returns a 500 server error.
        }
    )
    return response['data']['data']['attributes']['url']


async def has_webhook():
    """Investigates the existence of a webhook on Lemon Squeezy.

    It will check if a given webhook exists on Lemon Squeezy. If present, it
    returns that webhook, otherwise, it returns `None`.

    Returns:
        The found `Webhook`. Otherwise, `None`.

    Raises:
        `ValueError`: If a webhook url is not present in the environment variables.
    """
    configure_lemonsqueezy()

    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url is None:
        raise ValueError(
            "Missing required `WEBHOOK_URL` env variable. Please, set it in your"
            " .env file."
        )

    if not webhook_url.endswith("/"):
        webhook_url = f"{webhook_url}/"
    
    webhook_url = f"{webhook_url}api/webhook"
    
    webhooks = await list_webhooks({
        'filter': {
            'store_id': os.getenv("LEMONSQUEEZY_STORE_ID")
        }
    })

    webhook = cast(Webhook | None, next(filter(
        lambda x: 
            x['attributes']['url'] == webhook_url and x['attributes']['test_mode'],
        webhooks['data']['data']
    ), None))

    return webhook


async def setup_webhook():
    """Sets up a webhook on Lemon Squeezy.
    
    It sets a webhook on Lemon Squeezy only if one for the given url does not
    already exist. This webhook will then be used to listen for subscription
    events.

    Raises:
        `ValueError`: If a webhook url is not present in the environment variables.
    """
    configure_lemonsqueezy()

    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url is None:
        raise ValueError(
            "Missing required `WEBHOOK_URL` env variable. Please, set it in your"
            " .env file."
        )
    
    if not webhook_url.endswith("/"):
        webhook_url = f"{webhook_url}/"
    
    webhook_url = f"{webhook_url}api/webhook"

    print(f"Setting up a webhook on Lemon Squeezy (Test mode)...")

    webhook = await has_webhook()

    if webhook is None:
        new_webhook = await create_webhook(
            cast(str, os.getenv("LEMONSQUEEZY_STORE_ID")),
            {
                'secret': cast(str, os.getenv("LEMONSQUEEZY_WEBHOOK_SECRET")),
                'url': webhook_url,
                'test_mode': True,
                'events': [
                    'subscription_created',
                    'subscription_expired',
                    'subscription_updated',
                ]
            },
        )
        webhook = new_webhook['data']['data']

    print(f"Webhook {webhook['id']} created on Lemon Squeezy.")