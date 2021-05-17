# SoK - Yield Aggregators in DeFi

## yieldenv

Environment for yield generators

## Setup

### Clone the repo

```
git clone https://github.com/SimonCousaert/yieldAggregators
cd yieldAggregators
```

### Create a python virtual environment

- iOS

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

## Connect to a full node to fetch onchain data

```
ssh -L 8545:localhost:8545 satoshi.doc.ic.ac.uk
set -xg WEB3_PROVIDER_URI http://localhost:8545
```

## Git Large File Storage (Git LFS)

All files in [`data/`](data/) are stored with `lfs`:

```
git lfs track data/**/*
```
