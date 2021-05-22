import os
import gzip
import json
from yieldenv.constants import CONTRACT_DATA, DATA_PATH
from yieldenv.settings import PROJECT_ROOT
import pandas as pd

import matplotlib.pyplot as plt

IMAGE_PATH = os.path.join(PROJECT_ROOT, "assets")

BLOCK_NUMBER = "blocks"
VALUE = "pps"


# --------------- vault DAI supply ---------------------

for name, value in CONTRACT_DATA.items():
    if (value['asset'] == "DAI"):
        for key, func in value["function"].items():
            if (key == "total_supply"):
                result = {BLOCK_NUMBER: [], VALUE: []}
                with gzip.open(
                    os.path.join(
                        DATA_PATH, f"{value['protocol']}_{value['asset']}_{key}.jsonl.gz"
                    )
                ) as f:
                    for _, w in enumerate(f):
                        this_block = json.loads(w)
                        # if this_block[1] < 100:
                        #     next
                        result[BLOCK_NUMBER].append(this_block[0])
                        result[VALUE].append(this_block[1] / (10**int(value['decimals'])))
                    print(result[BLOCK_NUMBER][0])
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title)

plt.legend(loc='upper left')
fig_path = os.path.join(IMAGE_PATH, f"{title}.pdf")
plt.savefig(fig_path)
plt.show()
plt.close()


# ---------------  DAI price per share  ---------------------

for name, value in CONTRACT_DATA.items():
    if (value['asset'] == "DAI"):
        for key, func in value["function"].items():
            if (key == "price_per_share"):
                result = {BLOCK_NUMBER: [], VALUE: []}
                with gzip.open(
                    os.path.join(
                        DATA_PATH, f"{value['protocol']}_{value['asset']}_{key}.jsonl.gz"
                    )
                ) as f:
                    for _, w in enumerate(f):
                        this_block = json.loads(w)
                        if this_block[1] / 1e18 > 0.1:
                            result[BLOCK_NUMBER].append(this_block[0])
                            result[VALUE].append(this_block[1] / (10**int(value['decimals'])))
                    print(result[BLOCK_NUMBER][0])
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title)

plt.legend(loc='upper left')
fig_path = os.path.join(IMAGE_PATH, f"{title}.pdf")
plt.savefig(fig_path)
plt.show()
plt.close()

# --------------- vault USDC supply ---------------------

for name, value in CONTRACT_DATA.items():
    if (value['asset'] == "USDC"):
        for key, func in value["function"].items():
            if (key == "total_supply"):
                result = {BLOCK_NUMBER: [], VALUE: []}
                with gzip.open(
                    os.path.join(
                        DATA_PATH, f"{value['protocol']}_{value['asset']}_{key}.jsonl.gz"
                    )
                ) as f:
                    for _, w in enumerate(f):
                        this_block = json.loads(w)
                        # if this_block[1] < 100:
                        #     next
                        result[BLOCK_NUMBER].append(this_block[0])
                        result[VALUE].append(this_block[1] / (10**int(value['decimals'])))
                    print(result[BLOCK_NUMBER][0])
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title)

plt.legend(loc='upper left')
fig_path = os.path.join(IMAGE_PATH, f"{title}.pdf")
plt.savefig(fig_path)
plt.show()
plt.close()



# ---------------  USDC price per share  ---------------------

for name, value in CONTRACT_DATA.items():
    if (value['asset'] == "USDC"):
        for key, func in value["function"].items():
            if (key == "price_per_share"):
                result = {BLOCK_NUMBER: [], VALUE: []}
                with gzip.open(
                    os.path.join(
                        DATA_PATH, f"{value['protocol']}_{value['asset']}_{key}.jsonl.gz"
                    )
                ) as f:
                    for _, w in enumerate(f):
                        this_block = json.loads(w)
                        if this_block[1] / 1e6 > 0.1:
                            result[BLOCK_NUMBER].append(this_block[0])
                            result[VALUE].append(this_block[1] / 1e6)
                    print(result[BLOCK_NUMBER][0])
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title)

plt.legend(loc='upper left')
fig_path = os.path.join(IMAGE_PATH, f"{title}.pdf")
plt.savefig(fig_path)
plt.show()
plt.close()


# --------------- vault 3crv supply ---------------------

for name, value in CONTRACT_DATA.items():
    if (value['asset'] == "3crv"):
        for key, func in value["function"].items():
            if (key == "total_supply"):
                result = {BLOCK_NUMBER: [], VALUE: []}
                with gzip.open(
                    os.path.join(
                        DATA_PATH, f"{value['protocol']}_{value['asset']}_{key}.jsonl.gz"
                    )
                ) as f:
                    for _, w in enumerate(f):
                        this_block = json.loads(w)
                        # if this_block[1] < 100:
                        #     next
                        result[BLOCK_NUMBER].append(this_block[0])
                        result[VALUE].append(this_block[1] / (10**int(value['decimals'])))
                    print(result[BLOCK_NUMBER][0])
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title)

plt.legend(loc='upper left')
fig_path = os.path.join(IMAGE_PATH, f"{title}.pdf")
plt.savefig(fig_path)
plt.show()
plt.close()

# ---------------  3crv price per share  ---------------------

for name, value in CONTRACT_DATA.items():
    if (value['asset'] == "3crv"):
        for key, func in value["function"].items():
            if (key == "price_per_share"):
                result = {BLOCK_NUMBER: [], VALUE: []}
                with gzip.open(
                    os.path.join(
                        DATA_PATH, f"{value['protocol']}_{value['asset']}_{key}.jsonl.gz"
                    )
                ) as f:
                    for _, w in enumerate(f):
                        this_block = json.loads(w)
                        if this_block[1] / 1e18 > 0.1:
                            result[BLOCK_NUMBER].append(this_block[0])
                            result[VALUE].append(this_block[1] / 1e18)
                    print(result[BLOCK_NUMBER][0])
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title)

plt.legend(loc='upper left')
fig_path = os.path.join(IMAGE_PATH, f"{title}.pdf")
plt.savefig(fig_path)
plt.show()
plt.close()





# --------------------------------------------------------------

# result = {BLOCK_NUMBER: [], VALUE: []}
# for _, w in enumerate(harvest_dai_data):
#     this_block = json.loads(w)
#     result[BLOCK_NUMBER].append(this_block[0])
#     result[VALUE].append(this_block[1] / 1e24)

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
