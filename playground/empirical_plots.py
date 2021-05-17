import os
import gzip
import json
from yieldenv.constants import CONTRACT_DATA, DATA_PATH

import matplotlib.pyplot as plt

BLOCK_SERIES_NAME = "blocks"
PPS_SERIES_NAME = "pps"

for name, value in CONTRACT_DATA.items():
    result: dict[str, list[float]] = {BLOCK_SERIES_NAME: [], PPS_SERIES_NAME: []}
    with gzip.open(os.path.join(DATA_PATH, f"{name}_pricePerShare.jsonl.gz")) as f:
        for _, w in enumerate(f):
            this_block = json.loads(w)
            result[BLOCK_SERIES_NAME].append(this_block[0])
            result[PPS_SERIES_NAME].append(this_block[1])

plt.plot(result[BLOCK_SERIES_NAME], result[PPS_SERIES_NAME])
