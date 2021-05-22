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

axes_fontsize = 18
ticks_fontsize = 18
title_fontsize = 18
legend_title_fontsize = 17
legend_fontsize = 17
magnitude_fontsize = 16
ylim_lower = 0.82
ylim_upper = 1.065




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
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title, fontsize=title_fontsize)
                    
plt.xlabel(xlabel="Date", fontsize=axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.gca().yaxis.get_offset_text().set_size(magnitude_fontsize)
# plt.ylim(ylim_lower, ylim_upper)
plt.legend(
    loc='upper left',
    fontsize=legend_fontsize,
    title_fontsize=legend_title_fontsize,
    labelspacing=0.1,
    frameon=True,)
fig_path = os.path.join(IMAGE_PATH, f"vault_DAI_total_supply.pdf")
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
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title, fontsize=title_fontsize)

plt.xlabel(xlabel="Date", fontsize=axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.gca().yaxis.get_offset_text().set_size(magnitude_fontsize)
plt.ylim(ylim_lower, ylim_upper)
plt.legend(
    loc='lower left',
    fontsize=legend_fontsize,
    title_fontsize=legend_title_fontsize,
    labelspacing=0.1,
    frameon=True,)
fig_path = os.path.join(IMAGE_PATH, f"vault_DAI_price_per_share.pdf")
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
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title, fontsize=title_fontsize)

plt.xlabel(xlabel="Date", fontsize=axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.gca().yaxis.get_offset_text().set_size(magnitude_fontsize)
# plt.ylim(ylim_lower, ylim_upper)
plt.legend(
    loc='upper left',
    fontsize=legend_fontsize,
    title_fontsize=legend_title_fontsize,
    labelspacing=0.1,
    frameon=True,)
fig_path = os.path.join(IMAGE_PATH, f"vault_USDC_total_supply.pdf")
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
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title, fontsize=title_fontsize)

plt.xlabel(xlabel="Date", fontsize=axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.gca().yaxis.get_offset_text().set_size(magnitude_fontsize)
plt.ylim(ylim_lower, ylim_upper)
plt.legend(
    loc='center right',
    fontsize=legend_fontsize,
    title_fontsize=legend_title_fontsize,
    labelspacing=0.1,
    frameon=True,)
fig_path = os.path.join(IMAGE_PATH, f"vault_USDC_price_per_share.pdf")
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
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title, fontsize=title_fontsize)

plt.xlabel(xlabel="Date", fontsize=axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.gca().yaxis.get_offset_text().set_size(magnitude_fontsize)
# plt.ylim(ylim_lower, ylim_upper)
plt.legend(
    loc='upper right',
    fontsize=legend_fontsize,
    title_fontsize=legend_title_fontsize,
    labelspacing=0.1,
    frameon=True,)
fig_path = os.path.join(IMAGE_PATH, f"vault_3crv_total_supply.pdf")
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
                    date_range = pd.date_range(value['start_date'], value['end_date'], periods = len(result[BLOCK_NUMBER]))
                    plt.plot(date_range, result[VALUE], label = f"{value['protocol']}")
                    plt.gcf().autofmt_xdate()
                    title=f"vault{value['asset']}: {key}"
                    plt.title(title, fontsize=title_fontsize)

plt.xlabel(xlabel="Date", fontsize=axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.gca().yaxis.get_offset_text().set_size(magnitude_fontsize)
plt.ylim(ylim_lower, ylim_upper)
plt.legend(
    loc='lower left',
    fontsize=legend_fontsize,
    title_fontsize=legend_title_fontsize,
    labelspacing=0.1,
    frameon=True,)
fig_path = os.path.join(IMAGE_PATH, f"vault_3crv_price_per_share.pdf")
plt.savefig(fig_path)
plt.show()
plt.close()
