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
    """Retrieve a subscription.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for the subscription with the given id.

    Args:
        `subscription_id`: The given subscription id.
        `params`: (Optional) Additional parameters.
        `params['include']`: (Optional) Related resources.
    
    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `data` key holds the value of the subscription object requested.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
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
        `subscription_id`: The given subscription id.
        `update_subscription`: Information that needs to be updated.

    Returns:
        Response object with the keys `data`, `error` and `status_code`. The
        `data` key holds the subscription object.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
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
    """Cancel a subscription.

    Args:
        `subscription_id`: The given subscription id.
    
    Returns:
        Response object with the keys `data`, `error` and `status_code`. The
        `data` key holds the subscription object in a cancelled state.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
    options = FetchOptions(
        path=f"/v1/subscriptions/{subscription_id}",
        method=HTTPVerbEnum.DELETE,
    )
    return FetchResponse[Subscription](**await fetch(options)).model_dump()

async def list_subscriptions(params: dict = {}):
    """Retrieve a list of subscriptions.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for a list of subscriptions.

    Args:
        `params`: (Optional) Additional parameters.
        `params['filter']`: (Optional) Filter parameters.
        `params['filter']['store_id']`: (Optional) Only return subscriptions
        belonging to the store with this ID.
        `params['filter']['order_item_id']`: (Optional) Only return subscriptions
        belonging to the order item with this ID.
        `params['filter']['user_email']`: (Optional) Only return subscriptions
        where the `user_email` field is equal to this email address.
        `params['filter']['variant_id']`: (Optional) Only return subscriptions
        belonging to the variant with this ID.
        `params['filter']['order_id']`: (Optional) Only return subscriptions
        belonging to the order with this ID.
        `params['filter']['product_id']`: (Optional) Only return subscriptions
        belonging to the product with this ID.
        `params['page']`: (Optional) Custom paginated queries.
        `params['page']['number']`: (Optional) The parameter determine which page
        to retrieve.
        `params['page']['size']`: (Optional) The parameter to determine how many
        results to return per page.
        `params['include']`: (Optional) Related resources.

    Returns:
        Response object with the keys `data`, `error`, and `status_code`. The
        `data` key holds the paginated list of subscription objects ordered by
        `created_at` (descending).

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature or if the LemonSqueezy API response doesn't match the provided
        pydantic schema.
    """
    options = FetchOptions(
        path='/v1/subscriptions',
        param=params_to_query_string(ListSubscriptionParams(**params))
    )
    return FetchResponse[ListSubscriptions](**await fetch(options)).model_dump()