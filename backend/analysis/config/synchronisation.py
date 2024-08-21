import asyncio
import os

from typing import cast

from analysis.config import configure_lemonsqueezy
from analysis.models import Plan
from lemon.src.products import list_products, get_product
from lemon.src.prices import list_prices

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