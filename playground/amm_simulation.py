from yieldenv.env import Env, PriceDict, User, CPAmm
import matplotlib.pyplot as plt
import numpy as np
import random

"""
Storyline: investor provides LP tokens to a yield aggregator, which 
accrues yield by collecting trading fees + yield of a liquidity mining program +
potential loss through divergence loss
"""


def Randwalk(days: int, _start_price: float, _daily_change: float):

    y = _start_price
    price = [y]

    for _ in range(days):
        move = np.random.uniform(0, 1)

        if move < 0.5:  # go up
            y += _daily_change * y

        if move > 0.5:  # go down
            y -= _daily_change * y

        price.append(y)

    return price


def simulate_cpamm(
    _initial_supplied_funds_amm: dict,
    _startprice_quote_token: float,
    _percentage_liquidity_aggr: float,
    _startprice_governance_token: float,
    _gov_tokens_distributed_perday: float,
    _initial_funds_trader: dict = {"dai": 1e20, "eth": 1e20},
    _days_to_simulate: int = 365,
    _scenario: str = "benchmark",
):

    # initialization vars
    initial_reserves_amm = list(_initial_supplied_funds_amm.values())
    # the aggregator will later get and supply a percentage of the market funds
    initial_funds_aggr = _initial_supplied_funds_amm.copy()
    initial_funds_aggr.update(
        (x, y * _percentage_liquidity_aggr) for x, y in initial_funds_aggr.items()
    )

    # set up an environment with all DAI prices of 1, price for governance token
    simulation_env = Env(prices=PriceDict({"dai": 1, "eth": _startprice_quote_token}))

    # set up a user that represents (market - yield aggregator)
    market_maker = User(
        env=simulation_env,
        name="market_maker",
        funds_available=_initial_supplied_funds_amm,
    )

    # set up an amm pool with DAI-ETH - Initialized by the market maker
    dai_eth_amm = CPAmm(
        env=simulation_env,
        reward_token_name="sushi",
        fee=0.00002,
        initiator=market_maker,
        initial_reserves=initial_reserves_amm,
    )

    # set up a trader that aggregates trades in the market
    trader = User(
        env=simulation_env,
        name="trader",
        funds_available=_initial_funds_trader,
    )

    # create a user for the aggregator
    aggregator = User(
        env=simulation_env,
        name="aggregator",
        funds_available=initial_funds_aggr,
    )

    # aggregator supplies all funds into the amm pool
    aggregator.update_liquidity(
        dai_eth_amm.total_pool_shares * _percentage_liquidity_aggr, amm=dai_eth_amm
    )

    # create array of x days of returns
    returns = [0.0] * _days_to_simulate

    # simulate random walk for gov token price
    gov_token_prices = Randwalk(_days_to_simulate, _startprice_governance_token, 0.05)

    # simulate every day
    if _scenario == "benchmark":
        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)

            returns[i] = aggregator.wealth
    elif _scenario == "only buy":
        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            for m in range(50):
                trade_amount = random.randint(1, 1000000)
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=0)

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)

            returns[i] = aggregator.wealth
    elif _scenario == "only sell":
        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            for m in range(50):
                trade_amount = random.randint(1, 1000000)
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=1)

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)

            returns[i] = aggregator.wealth
    elif _scenario == "both":
        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            for m in range(25):
                trade_amount = random.randint(1, 1000000)
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=0)
            for n in range(25):
                trade_amount = random.randint(1, 1000000)
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=1)

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)

            returns[i] = aggregator.wealth
    else:
        print("Scenario not available")
        returns = None

    return returns


returns_benchmark = simulate_cpamm(
    _initial_supplied_funds_amm={"dai": 120000000, "eth": 30000},
    _startprice_quote_token=4000,
    _percentage_liquidity_aggr=0.01,
    _startprice_governance_token=30,
    _gov_tokens_distributed_perday=100,
    _days_to_simulate=365,
    _scenario="benchmark",
)

returns_only_buy = simulate_cpamm(
    _initial_supplied_funds_amm={"dai": 120000000, "eth": 30000},
    _startprice_quote_token=4000,
    _percentage_liquidity_aggr=0.01,
    _startprice_governance_token=30,
    _gov_tokens_distributed_perday=100,
    _days_to_simulate=365,
    _scenario="only buy",
)

returns_only_sell = simulate_cpamm(
    _initial_supplied_funds_amm={"dai": 120000000, "eth": 30000},
    _startprice_quote_token=4000,
    _percentage_liquidity_aggr=0.01,
    _startprice_governance_token=30,
    _gov_tokens_distributed_perday=100,
    _days_to_simulate=365,
    _scenario="only sell",
)

returns_both = simulate_cpamm(
    _initial_supplied_funds_amm={"dai": 120000000, "eth": 30000},
    _startprice_quote_token=4000,
    _percentage_liquidity_aggr=0.01,
    _startprice_governance_token=30,
    _gov_tokens_distributed_perday=100,
    _days_to_simulate=365,
    _scenario="both",
)

plt.plot(returns_benchmark, label="Benchmark")
plt.plot(returns_only_buy, label="Only buy")
plt.plot(returns_only_sell, label="Only sell")
plt.plot(returns_both, label="Both")
plt.legend(loc="best")
