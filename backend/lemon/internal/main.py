import asyncio

from request import fetch, FetchOptions
from setup import lemon_squeezy_setup, Config
from utils import get_kv, CONFIG_KEY

if __name__ == "__main__":
    from time import perf_counter_ns
    # time_a = perf_counter_ns()
    lemon_squeezy_setup(Config(api_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NGQ1OWNlZi1kYmI4LTRlYTUtYjE3OC1kMjU0MGZjZDY5MTkiLCJqdGkiOiJjM2ViOTNkNjZkNmExZDU5YTIxNjBhZDg5OWM2N2Y4YmYwZmJhZjQxZDRkZmVjNTM5MDE2MWM4MTlhNDg2MTlhYjc0NjYxMzZjYWU3NDI2ZiIsImlhdCI6MTcyMDAyNzMzMy4xMDk2MDcsIm5iZiI6MTcyMDAyNzMzMy4xMDk2MSwiZXhwIjoyMDM1NTYwMTMzLjA4MTE3OCwic3ViIjoiMjY1NDgxMiIsInNjb3BlcyI6W119.iV72blplnJCFLID9Idlf8ZdyLXwSXbWXQKM91BkLgJQZ3IWRjOJSDaom3gJCHB5VKOHQztmrvsOulPCgDOxEOjDPNc1SLc_MVSr-nhMIPBAwuQpBjdvwzu1LsLbPdkynZLsTO3Xx5yrszUNvtKoY3FCvZzSW4_oqjFp3F9pFaPPLbJVCBsnE6peSlgPln5x01tvb_bPpkZoeAA4HEPfZ4GCleqcuU4kCTexemsC-OndeuHMsD_jyogzGKymUgoys806WKJyCw80pfv6h6__-RvB8svXZBWJkvxurAVaJUiRszGMAsyj94OL-mXFK5xA09c47aQ9OL5FK6KRtP4xvkxA-e3Ownz9ex9xfunrs2iQcgFtmTNs-gC5PcapeAyuRZCQWYfAmHhgtZFQs7KRR1zfCQKSLyrJhwiOuNgzxFLAVI6D8dsHWrHnBTFdGo87p0b7-XXuH2r6YuqNm1hXg_5KTzTbeRYjOHwOikM8DCIIgxiv-low3zCB5B3NFQnnl"))
    # print(config)
    # print(get_kv(CONFIG_KEY))

    options = FetchOptions(
        path="/v1/checkouts",
        method="POST",  # type: ignore
        body={
            "data": {
                "type": "checkouts",
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
    print(val)
    print(f"Time elapsed: {duration:.2f}s")