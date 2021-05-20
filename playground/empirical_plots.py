import os
import gzip
import json
from yieldenv.constants import CONTRACT_DATA, DATA_PATH

import matplotlib.pyplot as plt

BLOCK_NUMBER = "blocks"
VALUE = "pps"

for name, value in CONTRACT_DATA.items():
    for key, func in value["function"].items():
        result = {BLOCK_NUMBER: [], VALUE: []}
        with gzip.open(
            os.path.join(
                DATA_PATH, f"{value['protocol']}_{value['asset']}_{key}.jsonl.gz"
            )
        ) as f:
            for _, w in enumerate(f):
                this_block = json.loads(w)
                if this_block[1] < 100:
                    next
                result[BLOCK_NUMBER].append(this_block[0])
                result[VALUE].append(this_block[1] / 1e24)
            plt.plot(result[BLOCK_NUMBER], result[VALUE])
            plt.title(f"{value['protocol']}_{value['asset']}_{key}")
            plt.show()
            plt.close()


# plt.plot(result[BLOCK_SERIES_NAME], result[PPS_SERIES_NAME])

#         get_onchain_data(
#             abi_address=value["abi_address"],
#             contract_address=value["contract_address"],
#             start_no=value["start_block"],
#             end_no=value["end_block"],
#             file_name=f"{value['protocol']}_{value['asset']}_{key}",
#             function_name=func,
#         )

# for name, value in CONTRACT_DATA.items():
#     result = {BLOCK_SERIES_NAME: [], PPS_SERIES_NAME: []}
#     with gzip.open(os.path.join(DATA_PATH, f"{name}_pricePerShare.jsonl.gz")) as f:
#         for _, w in enumerate(f):
#             this_block = json.loads(w)
#             result[BLOCK_SERIES_NAME].append(this_block[0])
#             result[PPS_SERIES_NAME].append(this_block[1])
