from os import path
from yieldenv.settings import PROJECT_ROOT

DATA_PATH = path.join(PROJECT_ROOT, "data")

INTEREST_TOKEN_PREFIX = "interest-"
DEBT_TOKEN_PREFIX = "debt-"

END_BLOCK = 12453546

FUNCTIONS_INTERESTED = ["total_asset", "total_supply", "price_per_share"]
# must all be checksum address!
CONTRACT_DATA = {
    "DAI yVault": {
        "protocal": "yearn",
        "asset": "DAI",
        "abi_address": "0xe11ba472F74869176652C35D30dB89854b5ae84D",
        "contract_addresse": "0x19D3364A399d251E894aC732651be8B0E4e85001",
        "start_block": 11673762,
        "end_block": END_BLOCK,
        "function": {
            FUNCTIONS_INTERESTED[0]: "totalAssets",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "pricePerShare",
        },
    }
}
