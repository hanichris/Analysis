import asyncio
import functools
import logging
import os
import sys

from typing import cast
from uuid import UUID

import httpx

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from analysis.models import Plan, User, WebhookEvent, Subscription
from analysis.config import (
    configure_lemonsqueezy,
    webhook_has_data,
    webhook_has_meta,
)

from lemon.src.prices import get_price

logger = logging.getLogger(__name__)

def async_to_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = asyncio.run(func(*args, **kwargs))
        return value
    return wrapper


@shared_task
@async_to_sync
async def process_webhook_event(webhook_event_pk):
    configure_lemonsqueezy()

    if os.getenv('WEBHOOK_URL') is None:
        logger.error(
            'Missing required WEBHOOK_URL env variable. Please, set it in'
            'your .env file.'
        )
        return
    
    webhook_event = await WebhookEvent.objects.aget(pk=webhook_event_pk)
    
    event_body = webhook_event.body
    processing_error = ''
    if not webhook_has_meta(event_body):
        processing_error = 'Event body is missing the `meta` property'
    elif webhook_has_data(event_body):
        if webhook_event.event_name.startswith('subscription_payment_'):
            pass
        elif webhook_event.event_name.startswith('subscription_'):
            user_id = event_body['meta']['custom_data']['user_id']
            attributes = event_body['data']['attributes']
            variant_id = int(attributes['variant_id'])
            price_id = attributes['first_subscription_item']['price_id']

            plan_task = None
            user_task = None
            try:
                async with asyncio.TaskGroup() as tg:
                    plan_task = tg.create_task(Plan.objects.aget(variant_id=variant_id))
                    user_task = tg.create_task(User.people.aget(pk=UUID(user_id)))
            except ExceptionGroup as exc:
                processing_error = exc.message

            plan = None
            user = None
            try:
                plan = plan_task.result() if plan_task else plan
                user = cast(User, user_task.result()) if user_task else user
            except (ObjectDoesNotExist, asyncio.CancelledError) as exc:
                processing_error = str(exc)

            if plan and user:
                response = await get_price(price_id)
                if response.get('error'):
                    processing_error = 'Failed to retrieve the price data for '
                    f'the subscription {event_body['data']['id']}'
                else:
                    is_usage_based = attributes[
                        'first_subscription_item'
                    ].get('is_usage_based')

                    price = response['data']['data']['attributes'][
                        'unit_price_decimal'
                    ] if is_usage_based else response['data']['data'][
                        'attributes'
                    ]['unit_price']

                    update_data = {
                        'lemonsqueezy_id': event_body['data']['id'],
                        'order_id': int(attributes['order_id']),
                        'name': attributes['user_name'],
                        'email': attributes['user_email'],
                        'status': attributes['status'],
                        'status_formatted': attributes['status_formatted'],
                        'renews_at': attributes['renews_at'],
                        'price': str(price) if price else '',
                        'subscription_item_id': attributes[
                            'first_subscription_item'
                        ]['id'],
                    }

                    if ends_at := attributes['ends_at']:
                        update_data['ends_at'] = ends_at
                    if trial_ends_at := attributes['trial_ends_at']:
                        update_data['trial_ends_at'] = trial_ends_at
                    if is_usage_based:
                        update_data['is_usage_based'] = is_usage_based
                    # has a conflict because of unique key constraint on the lemonsqueezy_id field.
                    new_subscription = Subscription(**update_data)
                    new_subscription.user = user
                    new_subscription.plan = plan
                    await new_subscription.asave()

        elif webhook_event.event_name.startswith('order_'):
            pass
        elif webhook_event.event_name.startswith('license_'):
            pass
    
    webhook_event.processed = True
    webhook_event.processing_error = processing_error
    await webhook_event.asave(update_fields=['processed', 'processing_error'])

@shared_task
@async_to_sync
async def send_to_zoho(data: dict):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(
            headers=headers,
            follow_redirects=True,
            timeout=None
        ) as client:
            res = await client.post(
                'https://crm.zoho.com/crm/WebToLeadForm',
                json=data
            )
            res.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        print(exc, file=sys.stderr)