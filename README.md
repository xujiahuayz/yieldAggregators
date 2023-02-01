# DeFi Yield Farming

Paper link:

> Cousaert, S., Xu, J., & Matsui, T. (2021). SoK: Yield Aggregators in DeFi. https://ieeexplore.ieee.org/abstract/document/9805523
> Xu, J. & Feng, Y. (2022). Reap the Harvest on Blockchain: A Survey of Yield Farming Protocols. https://doi.org/10.1109/TNSM.2022.3222815

## yieldenv

Environment for yield generators

## Setup

### Clone the repo

```
git clone https://github.com/xujiahuayz/yieldAggregators.git
cd yieldAggregators
```

### Create a python virtual environment

- Mac OS

```zsh
python3 -m venv venv
```

- Windows

```
python -m venv venv
```

### Activate the virtual environment

- iOS

```zsh
. venv/bin/activate
```

- Windows (in Command Prompt, NOT Powershell)

```zsh
venv\Scripts\activate.bat
```

## Install the project in editable mode

```
pip install -e ".[dev]"
```

## Connect to a full node to fetch on-chain data

Connect to a full node using `ssh` with port forwarding flag `-L` on:

### imperial node

```zsh
ssh -L 8545:localhost:8545 satoshi.doc.ic.ac.uk
```

Assign URI value to `WEB3_PROVIDER_URI` in a new terminal:

```zsh
set -xg WEB3_PROVIDER_URI http://localhost:8545
```

## Git Large File Storage (Git LFS)

All files in [`data/`](data/) are stored with `lfs`:

```
git lfs track data/**/*
```
