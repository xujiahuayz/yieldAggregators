import os
import gzip
import json

from yieldenv.fetcher import get_onchain_data
from yieldenv.constants import DATA_PATH


if __name__ == "__main__":
    os.environ.setdefault("WEB3_PROVIDER_URI", "http://localhost:8545")

    get_onchain_data(
        abi_address="0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C",
        contract_address="0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C",
        start_no=3_900_000,
        end_no=3_910_000,
        file_name="trial",
        function_name="totalSupply",
    )

    with gzip.open(os.path.join(DATA_PATH, "trial.jsonl.gz")) as f:
        for _, w in enumerate(f):
            this_block = json.loads(w)
            print(this_block)
