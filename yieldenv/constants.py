from os import path
from yieldenv.settings import PROJECT_ROOT
import pandas as pd

DATA_PATH = path.join(PROJECT_ROOT, "data")

INTEREST_TOKEN_PREFIX = "interest-"
DEBT_TOKEN_PREFIX = "debt-"

END_BLOCK = 13000000

FUNCTIONS_INTERESTED = ["total_asset", "total_supply", "price_per_share"]
# must all be checksum address!
CONTRACT_DATA = {
    "DAI yVault": {
        "protocol": "yearn",
        "asset": "DAI",
        "abi_address": "0xe11ba472F74869176652C35D30dB89854b5ae84D",
        "contract_address": "0x19D3364A399d251E894aC732651be8B0E4e85001",
        "start_block": 11673762,
        "start_date": pd.to_datetime("Jan-17-2021"),
        "start_block_proxy": 11616780,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 18,
        "function": {
            FUNCTIONS_INTERESTED[0]: "totalAssets",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "pricePerShare",
        },
    },
    "FARM_DAI": {
        "protocol": "harvest",
        "asset": "DAI",
        "abi_address": "0x9B3bE0cc5dD26fd0254088d03D8206792715588B",
        "contract_address": "0xab7FA2B2985BCcfC13c6D86b1D5A17486ab1e04C",
        "start_block": 11086832,
        "start_date": pd.to_datetime("Oct-19-2020"),
        "start_block_proxy": 10997712,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 18,
        "function": {
            FUNCTIONS_INTERESTED[0]: "underlyingBalanceWithInvestment",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "getPricePerFullShare",
        },
    },
    "IdleDAI_v4": {
        "protocol": "idle",
        "asset": "DAI",
        "abi_address": "0x2854A270FE9c839ffE453e9178d1cFeF109d6B8E",
        "contract_address": "0x3fE7940616e5Bc47b0775a0dccf6237893353bB4",
        "start_block": 10595640,
        "start_date": pd.to_datetime("Aug-04-2020"),
        "start_block_proxy": 12426425,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 18,
        "function": {
            # FUNCTIONS_INTERESTED[0]: FUNCTIONS_INTERESTED[1]*FUNCTIONS_INTERESTED[2],
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "tokenPrice",
        },
    },
    "USDC_yVault": {
        "protocol": "yearn",
        "asset": "USDC",
        "abi_address": "0xe11ba472F74869176652C35D30dB89854b5ae84D",
        "contract_address": "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9",
        "start_block": 11674456,
        "start_date": pd.to_datetime("Jan-17-2021"),
        "start_block_proxy": 11616780,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 6,
        "function": {
            FUNCTIONS_INTERESTED[0]: "totalAssets",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "pricePerShare",
        },
    },
    "FARM_USDC": {
        "protocol": "harvest",
        "asset": "USDC",
        "abi_address": "0x9B3bE0cc5dD26fd0254088d03D8206792715588B",
        "contract_address": "0xf0358e8c3CD5Fa238a29301d0bEa3D63A17bEdBE",
        "start_block": 11086842,
        "start_date": pd.to_datetime("Oct-19-2020"),
        "start_block_proxy": 10997712,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 6,
        "function": {
            FUNCTIONS_INTERESTED[0]: "underlyingBalanceWithInvestment",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "getPricePerFullShare",
        },
    },
    "Idle_USDC": {
        "protocol": "idle",
        "asset": "USDC",
        "abi_address": "0x2854A270FE9c839ffE453e9178d1cFeF109d6B8E",
        "contract_address": "0xF34842d05A1c888Ca02769A633DF37177415C2f8",
        "start_block": 10627792,
        "start_date": pd.to_datetime("Aug-09-2020"),
        "start_block_proxy": 12342939,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 18,
        "function": {
            # FUNCTIONS_INTERESTED[0]: FUNCTIONS_INTERESTED[1]*FUNCTIONS_INTERESTED[2],
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "tokenPrice",
        },
    },
    "Curve_3pool_yVault": {
        "protocol": "yearn",
        "asset": "3crv",
        "abi_address": "0xA696a63cc78DfFa1a63E9E50587C197387FF6C7E",
        "contract_address": "0x84E13785B5a27879921D6F685f041421C7F482dA",
        "start_block": 12245666,
        "start_date": pd.to_datetime("Apr-15-2021"),
        "start_block_proxy": 12185982,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 18,
        "function": {
            FUNCTIONS_INTERESTED[0]: "totalAssets",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "pricePerShare",
        },
    },
    "FARM_3Crv": {
        "protocol": "harvest",
        "asset": "3crv",
        "abi_address": "0x9B3bE0cc5dD26fd0254088d03D8206792715588B",
        "contract_address": "0x71B9eC42bB3CB40F017D8AD8011BE8e384a95fa5",
        "start_block": 11159005,
        "start_date": pd.to_datetime("Oct-30-2020"),
        "start_block_proxy": 10997712,
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 18,
        "function": {
            FUNCTIONS_INTERESTED[0]: "underlyingBalanceWithInvestment",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "getPricePerFullShare",
        },
    },
    "Pickle_3crv": {
        "protocol": "pickle",
        "asset": "3crv",
        "abi_address": "0x1BB74b5DdC1f4fC91D6f9E7906cf68bc93538e33",
        "contract_address": "0x1BB74b5DdC1f4fC91D6f9E7906cf68bc93538e33",
        "start_block": 11010885,
        "start_date": pd.to_datetime("Oct-07-2020"),
        "end_block": END_BLOCK,
        "end_date": pd.to_datetime("May-17-2021"),
        "decimals": 18,
        "function": {
            FUNCTIONS_INTERESTED[0]: "balance",
            FUNCTIONS_INTERESTED[1]: "totalSupply",
            FUNCTIONS_INTERESTED[2]: "getRatio",
        },
    },
}
