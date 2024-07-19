import asyncio
import pprint
import os
from dotenv import load_dotenv
from pathlib import Path
from time import perf_counter_ns

from lemon.internal.request import fetch, FetchOptions
from lemon.internal.setup import lemon_squeezy_setup, Config

def main():
    BASE_DIR = Path(__file__).resolve().parent

    load_dotenv(os.path.join(BASE_DIR, '.env'))

    lemon_squeezy_setup(Config(
        api_key=os.getenv("LEMONSQUEEZY_API_KEY"),
        on_error=lambda x: print(x)
    ))

    options = FetchOptions(
        path="/v1/checkouts",
        method="POST",  # type: ignore
        body={
            "data": {
                "type": "checkouts",
                "attributes": {
                    "checkout_data": {
                        "email": "hello@example.com",
                        "name": "Luke Skywalker",
                        "custom": {
                            "user_id": "123",
                        }
                    },
                },
                "relationships": {
                    "store": {
                        "data": {
                            "type": "stores",
                            "id": "106796"
                        }
                    },
                    "variant": {
                        "data": {
                            "type": "variants",
                            "id": "437953"
                        }
                    }
                },
            }
        }
    )
    time_a = perf_counter_ns()
    val = asyncio.run(fetch(options))
    time_b = perf_counter_ns()
    duration = (time_b - time_a) / 1e9
    pprint.pprint(val)
    print(f"Time elapsed: {duration:.2f}s")

if __name__ == "__main__":
    main()