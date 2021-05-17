from os import path
from yieldenv.settings import PROJECT_ROOT

DATA_PATH = path.join(PROJECT_ROOT, "data")

INTEREST_TOKEN_PREFIX = "interest-"
DEBT_TOKEN_PREFIX = "debt-"

END_BLOCK = 12453546
# must all be checksum address!
CONTRACT_DATA = {
    "yearn": {
        "abi_address": "0xe11ba472F74869176652C35D30dB89854b5ae84D",
        "contract_addresse": "0x19D3364A399d251E894aC732651be8B0E4e85001",
        "start_block": 11673762,
        "end_block": END_BLOCK,
    }
}
