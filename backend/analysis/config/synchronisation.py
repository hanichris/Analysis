import asyncio
import os

from functools import cmp_to_key
from operator import attrgetter
from typing import cast

from .util import cache_results, del_cache_key
from .lemonsqueezy import configure_lemonsqueezy

from analysis.models import Plan, User, Subscription
from lemon.src.products import list_products, get_product
from lemon.src.prices import list_prices
from lemon.src.checkouts import create_checkout
from lemon.src.webhooks import create_webhook, list_webhooks, Webhook
from lemon.src.subscriptions import get_subscription, cancel_subscription, update_subscription


f = attrgetter('status')

def custom_order(a, b):
    if f(a) == 'active' and f(b) == 'active':
        return -1
    if f(a) == 'paused' and f(b) == 'cancelled':
        return -1
    return 0

async def sync_plans() -> list[Plan] | None:
    """Synchronises the product variants from Lemon Squeezy with the database.

    Only synchronises the `subscription` variants. If there were variants
    obtained from Lemon Squeezy, then they are made available to the caller.

    Returns:
        (list[Plan] | None): The saved plan objects if there were any variants
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
        variant_obj['interval'] = current_price_obj['attributes']['renewal_interval_unit'] or ''
        variant_obj['interval_count'] = current_price_obj['attributes']['renewal_interval_quantity']
        variant_obj['trial_interval'] = current_price_obj['attributes']['trial_interval_unit'] or ''
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
                    'user_id': user.pk,
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

async def get_subscription_urls(id: str):
    """Retrieve the subscription urls related to a given subscription id.

    Retrieves the `update_payment_method` and `custom_portal` urls for the provided
    subscription id.
    Args:
        id: The subscription id of interest.
    Returns:
        dict: Holds the urls for the `update_payment_method` and `custom_portal`
        under the corresponding dictionary key.
    Raises:
        RuntimeError: If an error was encountered during the fetch request.
        ValidationError: If the data returned does not match the expected schema.
    """
    configure_lemonsqueezy()

    response = await get_subscription(id)

    return response['data']['data']['attributes']['urls']

@cache_results(timeout=60)
async def get_user_subscriptions(user: User):
    """Retrieves the subscriptions for a particular user.

    The retrieved subscriptions are ordered based on their status, i.e.
    1. Active Subscriptions
    2. Paused Subscriptions
    3. Cancelled Subscriptions
    Args:
        user: The user whose subscriptions are to be obtained.
    Returns:
        list: All the subscriptions for the given user.
    """
    subs = [
        sub
        async for sub in
        Subscription.objects.filter(user=user).select_related('plan')
    ]
    return sorted(subs, key=cmp_to_key(custom_order))


async def cancel_sub(sub_id: str, user: User):
    """Cancels the subscription identified by the given id for the particular user.

    Makes a delete request to lemon squeezy for the subscription with the given id.
    The api responds with a cancelled subscription object which is then used to
    update the corresponding subscription entry in the database.
    Args:
        sub_id: id for a particular subscription object.
        user: The user whose subscription is to be cancelled.
    Raises:
        RuntimeError: If a given subscription object is not found.
        ValidationError: If the response does not match the expected data schema.
    """
    configure_lemonsqueezy()

    user_subs: list[Subscription] = await get_user_subscriptions(user)
    sub = next(filter(lambda x: x.lemonsqueezy_id == sub_id , user_subs), None)
    if sub is None:
        raise RuntimeError(f"Subscription {sub_id} not found.")
    cancelled_sub = await cancel_subscription(sub.lemonsqueezy_id)

    sub.status=cancelled_sub['data']['data']['attributes']['status']
    sub.status_formatted=cancelled_sub['data']['data']['attributes']['status_formatted']
    if ends_at:=cancelled_sub['data']['data']['attributes']['ends_at']:
        sub.ends_at=ends_at
    await sub.asave(update_fields=['status, status_formatted, ends_at'])
    await del_cache_key(get_user_subscriptions)(user)
    
async def pause_sub(sub_id: str, user: User):
    """Pauses the subscription identified by the given id for the particular user.
    
    Makes a patch request to lemon squeezy with update details for for the
    subscription with the given id. The api responds with an updated subscription
    object which is then used to update the corresponding subscription entry in
    the database.
    Args:
        sub_id: id for a particular subscription object.
        user: The user whose subscription is to be paused.
    Raises:
        RuntimeError: If a given subscription object is not found.
        ValidationError: If the response does not match the expected data schema.
    """
    configure_lemonsqueezy()

    user_subs: list[Subscription] = await get_user_subscriptions(user)
    sub = next(filter(lambda x: x.lemonsqueezy_id == sub_id , user_subs), None)
    if sub is None:
        raise RuntimeError(f"Subscription {sub_id} not found.")
    paused_sub = await update_subscription(sub.lemonsqueezy_id, {
        'pause': {
            'mode': 'void',
        },
    })

    sub.status=paused_sub['data']['data']['attributes']['status']
    sub.status_formatted=paused_sub['data']['data']['attributes']['status_formatted']
    if ends_at:=paused_sub['data']['data']['attributes']['ends_at']:
        sub.ends_at=ends_at
    sub.is_paused=paused_sub['data']['data']['attributes']['pause'] is not None
    await sub.asave(update_fields=['status', 'status_formatted', 'ends_at', 'is_paused'])
    await del_cache_key(get_user_subscriptions)(user)

async def unpause_sub(sub_id: str, user: User):
    """Resumes a given subscription for a particular user.
    
    Makes a patch request to lemon squeezy with update details for the
    subscription with the given id. The api responds with an updated subscription
    object which is then used to update the corresponding subscription entry in
    the database.
    Args:
        sub_id: id for a particular subscription object.
        user. The user whose subscription is to be resumed.
    Raises:
        RuntimeError: If a given subscription object is not found.
        ValidationError: If the response does not match the expected data schema.
    """
    configure_lemonsqueezy()

    user_subs: list[Subscription] = await get_user_subscriptions(user)
    sub = next(filter(lambda x: x.lemonsqueezy_id == sub_id , user_subs), None)
    if sub is None:
        raise RuntimeError(f"Subscription {sub_id} not found.")
    
    resumed_sub = await update_subscription(sub.lemonsqueezy_id, {
        'pause': None,
    })

    sub.status=resumed_sub['data']['data']['attributes']['status']
    sub.status_formatted=resumed_sub['data']['data']['attributes']['status_formatted']
    if ends_at:=resumed_sub['data']['data']['attributes']['ends_at']:
        sub.ends_at=ends_at
    sub.is_paused=resumed_sub['data']['data']['attributes']['pause'] is not None
    await sub.asave(update_fields=['status', 'status_formatted', 'ends_at', 'is_paused'])
    await del_cache_key(get_user_subscriptions)(user)

async def change_plan(current_plan_id: int, new_plan_id: int, user: User):
    """Changes the plan for the user's current subscription.

    Makes a patch request to lemon squeezy with the update details for the
    subscription with the given id. The api responds with an updated subscription
    object which is then used to update the corresponding subscription entry in
    the database.
    Args:
        current_plan_id: The corresponding plan id for the current subscription.
        new_plan_id: The plan id to change the current subscription to.
        user: The user whose subscription is to be changed.
    Raises:
        RuntimeError: If a given subscription or plan object is not found.
        ValidationError: If the response does not match the expected data schema.
    """
    configure_lemonsqueezy()

    user_subs: list[Subscription] = await get_user_subscriptions(user)
    current_sub = cast(Subscription | None, next(
        filter(lambda x: x.plan.pk == current_plan_id, user_subs),
        None
    ))
    if current_sub is None:
        raise RuntimeError(
            f'No subscription with plan id: {current_plan_id} was found.'
        )
    
    try:
        new_plan = await Plan.objects.aget(pk=new_plan_id)
    except Plan.DoesNotExist:
        raise RuntimeError(f'No plan with id: {new_plan_id} was found.')
    
    updated_sub = await update_subscription(current_sub.lemonsqueezy_id, {
        'variant_id': new_plan.variant_id
    })

    
    current_sub.price = new_plan.price
    current_sub.plan = new_plan
    if ends_at:=updated_sub['data']['data']['attributes']['ends_at']:
        current_sub.ends_at = ends_at
    
    await current_sub.asave(update_fields=['price', 'plan', 'ends_at'])
    await del_cache_key(get_user_subscriptions)(user)
