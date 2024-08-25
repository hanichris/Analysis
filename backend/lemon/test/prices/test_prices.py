import os
import unittest

from numbers import Number
from pathlib import Path

from dotenv import load_dotenv

from src.internal.setup import lemon_squeezy_setup, Config
from src.prices import list_prices, get_price


class TestListPrices(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `list_prices` function"""

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))
    
    async def test_list_all_prices(self):
        """Tests that a paginated list of prices is returned."""
        response = await list_prices()
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list[dict] = response['data']['data']
        links: dict = response['data']['links']
        meta: dict =  response['data']['meta']

        self.assertTrue(meta.get('page'))
        self.assertIsInstance(data, list)
        self.assertTrue(links['first'])
        self.assertTrue(links['last'])

        entries = [
            meta['page']['currentPage'],
            meta['page']['from'],
            meta['page']['lastPage'],
            meta['page']['perPage'],
            meta['page']['to'],
            meta['page']['total'],
        ]
        for entry in entries:
            self.assertIsInstance(entry, Number)
        
        self.assertEqual(len(meta['page']), len(entries))

        variant = data[0]['relationships']['variant']
        self.assertTrue(variant['links'])
    
    async def test_filter_parameter(self):
        """Test should return a paginated list of prices filtered by variant_id"""
        variant_id = 437958
        response = await list_prices({
            "filter": {
                "variant_id": variant_id,
            },
        })
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: list[dict] = response['data']['data']
        links: dict = response['data']['links']
        meta: dict =  response['data']['meta']

        self.assertTrue(meta.get('page'))
        self.assertIsInstance(data, list)
        self.assertTrue(links['first'])
        self.assertTrue(links['last'])

        filtered_data = [
            item for item in filter(
                lambda x: x['attributes']['variant_id'] == variant_id,
                data
            )
        ]
        self.assertEqual(len(data), len(filtered_data))



class TestGetPrice(unittest.IsolatedAsyncioTestCase):
    """Test the functionality of the `get_price` function. """

    def setUp(self) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(os.path.join(BASE_DIR, '.env'))

        lemon_squeezy_setup(Config(
            api_key= os.getenv("LEMONSQUEEZY_API_KEY"),
        ))
    
    async def test_get_price_object(self):
        """Test should return the corresponding price object given the price id"""
        price_id = 646468
        variant_id = 437958
        response = await get_price(price_id)
        self.assertEqual(response.get('status_code'), 200)
        self.assertIsNone(response.get('error'))
        self.assertTrue(response.get('data'))

        data: dict = response['data']['data']
        links: dict = response['data']['links']

        self.assertTrue(data)
        self.assertEqual(
            links['self'],
            f"https://api.lemonsqueezy.com/v1/prices/{price_id}"
        )

        _id = data['id']
        _type = data['type']
        relationships = data['relationships']
        attributes = data['attributes']

        self.assertEqual(_id, str(price_id))
        self.assertEqual(_type, "prices")
        self.assertTrue(relationships)
        self.assertTrue(attributes)

        items = [
            attributes['category'],
            attributes['created_at'],
            attributes['min_price'],
            attributes['package_size'],
            attributes['renewal_interval_quantity'],
            attributes['renewal_interval_unit'],
            attributes['scheme'],
            attributes['setup_fee'],
            attributes['setup_fee_enabled'],
            attributes['suggested_price'],
            attributes['tax_code'],
            attributes['tiers'],
            attributes['trial_interval_quantity'],
            attributes['trial_interval_unit'],
            attributes['unit_price'],
            attributes['unit_price_decimal'],
            attributes['updated_at'],
            attributes['usage_aggregation'],
            attributes['variant_id'],
        ]

        for item in items:
            if item:
                self.assertIsInstance(item, bool | str | Number)
        self.assertEqual(attributes['variant_id'], variant_id)
        self.assertEqual(len(attributes), len(items))

        variant = relationships['variant']
        self.assertTrue(variant['links'])