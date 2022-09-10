# %%
import pandas as pd
import matplotlib.pyplot as plt
from yieldenv.constants import DATA_PATH
from os import path

# %%
df = pd.read_csv(path.join(DATA_PATH, "all.csv"))

df_YA = df[df["Category"] == "Yield Aggregator"]

# %%
df_YA

# %%
df_YA["Category.1"].unique()

# %%
df_YA_TVL = df_YA[df_YA["Category.1"] == "TVL"]

# %%
df_YA_TVL

# %%
df_bsc = df_YA_TVL[df_YA_TVL["Chain"] == "bsc"]
df_eth = df_YA_TVL[df_YA_TVL["Chain"] == "ethereum"]
df_pol = df_YA_TVL[df_YA_TVL["Chain"] == "polygon"]

# %%
df_time = pd.DataFrame(df.loc[0])

# %%
bsc = pd.concat([df_time.T, df_bsc])
bsc_buffer = bsc.drop(
    columns=["Unnamed: 0", "Category", "Chain", "Category.1", "Token"]
)
bsc_buffer = bsc_buffer.transpose()
bsc_buffer["date"] = pd.to_datetime(bsc_buffer.loc[:, 0])
bsc_buffer = bsc_buffer.drop(bsc_buffer.columns[[0]], axis=1)
bsc_buffer = bsc_buffer.set_index("date")
bsc_buffer = bsc_buffer.fillna(0)
bsc_TVL = bsc_buffer.sum(axis=1, skipna=True)


# %%
eth = pd.concat([df_time.T, df_eth])
eth_buffer = eth.drop(
    columns=["Unnamed: 0", "Category", "Chain", "Category.1", "Token"]
)
eth_buffer = eth_buffer.transpose()
eth_buffer["date"] = pd.to_datetime(eth_buffer.loc[:, 0])
eth_buffer = eth_buffer.drop(eth_buffer.columns[[0]], axis=1)
eth_buffer = eth_buffer.set_index("date")
eth_buffer = eth_buffer.fillna(0)
eth_TVL = eth_buffer.sum(axis=1, skipna=True)


# %%
pol = pd.concat([df_time.T, df_pol])
pol_buffer = pol.drop(
    columns=["Unnamed: 0", "Category", "Chain", "Category.1", "Token"]
)
pol_buffer = pol_buffer.transpose()
save_for_later = pol_buffer.loc[:, 0]
pol_buffer["date"] = pd.to_datetime(pol_buffer.loc[:, 0])
pol_buffer = pol_buffer.drop(pol_buffer.columns[[0]], axis=1)
pol_buffer = pol_buffer.set_index("date")
pol_buffer = pol_buffer.fillna(0)
pol_TVL = pol_buffer.sum(axis=1, skipna=True)


# %%
import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = "bsc", "ethereum", "polygon"
sizes = [bsc_TVL[-1], eth_TVL[-1], pol_TVL[-1]]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

# %%
labels = save_for_later
fig, ax = plt.subplots()

ax.bar(labels, eth_TVL, label="eth")
ax.bar(labels, bsc_TVL, bottom=eth_TVL, label="bsc")
ax.bar(labels, pol_TVL, bottom=eth_TVL + bsc_TVL, label="pol")


# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
ax.legend()

plt.show()
