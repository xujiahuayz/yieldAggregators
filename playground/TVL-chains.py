import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

from yieldenv.constants import DATA_PATH
from yieldenv.settings import PROJECT_ROOT

from os import path


# Filter out desired data
df = pd.read_csv(path.join(DATA_PATH, "all.csv"))
df_YA = df[df["Category"] == "Yield Aggregator"]
df_YA_TVL = df_YA[df_YA["Category.1"] == "TVL"]

df_bsc = df_YA_TVL[df_YA_TVL["Chain"] == "bsc"]
df_eth = df_YA_TVL[df_YA_TVL["Chain"] == "ethereum"]
df_pol = df_YA_TVL[df_YA_TVL["Chain"] == "polygon"]


# Clean the data
df_time = pd.DataFrame(df.loc[0])

bsc = pd.concat([df_time.T, df_bsc])
bsc_buffer = bsc.drop(
    columns=["Unnamed: 0", "Category", "Chain", "Category.1", "Token"]
)
bsc_buffer = bsc_buffer.transpose()
bsc_buffer["date"] = pd.to_datetime(bsc_buffer.loc[:, 0], format="%d/%m/%Y")
bsc_buffer = bsc_buffer.drop(bsc_buffer.columns[[0]], axis=1)
bsc_buffer = bsc_buffer.set_index("date")
bsc_buffer = bsc_buffer.fillna(0)
bsc_TVL = bsc_buffer.sum(axis=1, skipna=True)

eth = pd.concat([df_time.T, df_eth])
eth_buffer = eth.drop(
    columns=["Unnamed: 0", "Category", "Chain", "Category.1", "Token"]
)
eth_buffer = eth_buffer.transpose()
eth_buffer["date"] = pd.to_datetime(eth_buffer.loc[:, 0], format="%d/%m/%Y")
eth_buffer = eth_buffer.drop(eth_buffer.columns[[0]], axis=1)
eth_buffer = eth_buffer.set_index("date")
eth_buffer = eth_buffer.fillna(0)
eth_TVL = eth_buffer.sum(axis=1, skipna=True)

pol = pd.concat([df_time.T, df_pol])
pol_buffer = pol.drop(
    columns=["Unnamed: 0", "Category", "Chain", "Category.1", "Token"]
)
pol_buffer = pol_buffer.transpose()
pol_buffer["date"] = pd.to_datetime(pol_buffer.loc[:, 0], format="%d/%m/%Y")
pol_buffer = pol_buffer.drop(pol_buffer.columns[[0]], axis=1)
pol_buffer = pol_buffer.set_index("date")
pol_buffer = pol_buffer.fillna(0)
pol_TVL = pol_buffer.sum(axis=1, skipna=True)


eth_TVL_drop = eth_TVL.drop(eth_TVL.index[:424])
bsc_TVL_drop = bsc_TVL.drop(bsc_TVL.index[:424])
pol_TVL_drop = pol_TVL.drop(pol_TVL.index[:424])

# Define units function for plots
def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return "$%.2f%s " % (num, ["", "K", "M", "B", "T", "P"][magnitude])


# Draw the plot
fig, ax = plt.subplots(figsize=(7, 4))


mdates_x = mdates.date2num(pol_TVL_drop.index)


ax.bar(mdates_x, eth_TVL_drop, label="Ethereum", width=1)
ax.bar(mdates_x, bsc_TVL_drop, bottom=eth_TVL_drop, label="BNB Chain", width=1)
ax.bar(
    mdates_x, bsc_TVL_drop, bottom=eth_TVL_drop + bsc_TVL_drop, label="Polygon", width=1
)

ax.yaxis.set_major_formatter(human_format)


maj_loc = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(maj_loc)

fmt = mdates.ConciseDateFormatter(mdates_x)
ax.get_xaxis().set_major_formatter(fmt)


ax.set_ylabel("TVL")
ax.set_xlabel("Date")


ax.legend()


fig_path = path.join(PROJECT_ROOT, f"assets/TVL.pdf")
fig.savefig(fig_path)
plt.show()
plt.close()
