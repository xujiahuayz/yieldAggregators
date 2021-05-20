import os
import json
import gzip
from yieldenv.constants import DATA_PATH, CONTRACT_DATA, FUNCTIONS_INTERESTED

from web3.auto.http import w3

from eth_tools.abi_fetcher import fetch_abi
from eth_tools.contract_caller import ContractCaller


def get_onchain_data(
    abi_address: str,
    contract_address: str,
    start_no: int,
    end_no: int,
    file_name: str,
    function_name: str = FUNCTIONS_INTERESTED[2],
):
    abi = fetch_abi(abi_address)
    contract = w3.eth.contract(abi=abi, address=contract_address)
    contract_caller = ContractCaller(contract)
    results = contract_caller.collect_results(
        function_name,
        start_block=start_no,
        end_block=end_no,
        block_interval=500,
    )
    with gzip.open(os.path.join(DATA_PATH, f"{file_name}.jsonl.gz"), "wt") as f:
        for result in results:
            print(json.dumps(result), file=f)


if __name__ == "__main__":

    os.environ.setdefault("WEB3_PROVIDER_URI", "http://localhost:8545")

    for name, value in CONTRACT_DATA.items():
        for key, func in value["function"].items():
            get_onchain_data(
                abi_address=value["abi_address"],
                contract_address=value["contract_address"],
                start_no=value["start_block"],
                end_no=value["end_block"],
                file_name=f"{value['protocol']}_{value['asset']}_{key}",
                function_name=func,
            )
