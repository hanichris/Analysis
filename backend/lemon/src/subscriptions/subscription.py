from ..internal.request import fetch, FetchOptions, FetchResponse, HTTPVerbEnum
from ..internal.utils import include_to_query_string, params_to_query_string
from .types import (
    GetSubscriptionParams,
    ListSubscriptions,
    ListSubscriptionParams,
    Subscription,
    UpdateSubscription,
)

async def get_subscription(subscription_id: int | str, params: dict = {}):
    """"""
    options = FetchOptions(
        path=f"/v1/subscriptions/{subscription_id}",
        param=include_to_query_string(
            GetSubscriptionParams(**params).include
        )
    )
    return FetchResponse[Subscription](**await fetch(options)).model_dump()

async def updated_subscription(
        subscription_id: int | str,
        update_subscription: UpdateSubscription
):
    """Update a subscription.

    Makes a `PATCH` request with a set of parameters encoding the information to
    update lemonSqueezy API pertaining to a given subscription identified with the
    provided id.

    Args:
        subscription_id: The given subscription id.
        update_subscription: Information that needs to be updated.
    
    Returns:
        Response object with the keys `data`, `error` and `status_code`. The
        `data` key holds the subscription object.
    
    Raises:
        ValidationError: 

    """
    attributes = {
        'variant_id': update_subscription.get('variant_id'),
        'cancelled': update_subscription.get('cancelled'),
        'billing_anchor': update_subscription.get('billing_anchor'),
        'invoice_immediately': update_subscription.get('invoice_immediately'),
        'disable_prorations': update_subscription.get('disable_prorations'),
        'pause': update_subscription.get('pause'),
        'trial_ends_at': update_subscription.get('trial_ends_at')
    }

    options = FetchOptions(
        path=f"/v1/subscriptions/{subscription_id}",
        method=HTTPVerbEnum.PATCH,
        body={
            'data': {
                'type': 'subscriptions',
                'id': str(subscription_id),
                'attributes': attributes,
            }
        }
    )

    return FetchResponse[Subscription](**await fetch(options)).model_dump()

async def cancel_subscription(subscription_id: int | str):
    """"""
    options = FetchOptions(
        path=f"/v1/subscriptions/{subscription_id}",
        method=HTTPVerbEnum.DELETE,
    )
    return FetchResponse[Subscription](**await fetch(options)).model_dump()

async def list_subscriptions(params: dict = {}):
    options = FetchOptions(
        path='/v1/subscriptions',
        param=params_to_query_string(ListSubscriptionParams(**params))
    )
    return FetchResponse[ListSubscriptions](**await fetch(options)).model_dump()