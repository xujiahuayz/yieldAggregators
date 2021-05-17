from yieldenv.env import Env, PriceDict, User, CPAmm
import matplotlib.pyplot as plt
import numpy as np

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

    print(aggregator.funds_available)

    # aggregator supplies all funds into the amm pool
    aggregator.update_liquidity(
        dai_eth_amm.total_pool_shares * _percentage_liquidity_aggr, amm=dai_eth_amm
    )

    # create array of x days of returns
    returns = [0.0] * _days_to_simulate

    # simulate random walk for gov token price
    gov_token_prices = Randwalk(365, _startprice_governance_token, 0.05)

    # simulate every day
    for i in range(_days_to_simulate):
        simulation_env.prices["sushi"] = gov_token_prices[i]
        print("before---------------------------------")

        trader.sell_to_amm(dai_eth_amm, 1000000, sell_index=1)

        # dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)
        returns[i] = aggregator.wealth

    return returns


returns_1 = simulate_cpamm(
    {"dai": 120000000, "eth": 30000}, 4000, 0.01, 40, 100, _days_to_simulate=5
)

# returns_2 = simulate_simple_lending(100, 500000000, 0.8, 0.007, 0.06, 0.08, 100, 365)
# returns_3 = simulate_simple_lending(10, 500000000, 0.8, 0.007, 0.06, 0.08, 100, 365)
plt.plot(returns_1, label="Highest start price")
# plt.plot(returns_2, label="Medium start price")
# plt.plot(returns_3, label="Lowest start price")
# plt.legend(loc="lower right")

# random walk for gov token price
