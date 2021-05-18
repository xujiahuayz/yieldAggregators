from yieldenv.utils import PriceDict
from yieldenv.env import Env, User, Plf
import matplotlib.pyplot as plt
import numpy as np


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


def simulate_simple_lending(
    _startprice_governance_token: float,
    _initial_funds_plf: float,
    _initial_borrow_ratio: float,
    _aggregator_percentage_liquidyt_plf: float,
    _supply_apy_plf: float,
    _borrow_apy_plf: float,
    _gov_tokens_distributed_perday: float,
    _days_to_simulate: int = 365,
):

    # initialization vars
    initial_supplied_funds_plf = _initial_funds_plf
    initial_borrowed_funds = _initial_borrow_ratio * initial_supplied_funds_plf
    initial_supplied_funds_aggr = (
        _aggregator_percentage_liquidyt_plf * initial_supplied_funds_plf
    )
    days_to_simulate = _days_to_simulate

    # set up an environment with all DAI prices of 1, price for governance token
    simulation_env = Env(prices=PriceDict({"dai": 1}))

    # set up a user that represents (market - yield aggregator): give 500M DAI
    market_maker = User(
        env=simulation_env,
        name="market_maker",
        funds_available={"dai": initial_supplied_funds_plf},
    )

    # set up a plf pool with DAI - Initialized by the market maker with 500M DAI
    dai_plf = Plf(
        env=simulation_env,
        reward_token_name="aave",
        initiator=market_maker,
        initial_starting_funds=initial_supplied_funds_plf,
        supply_apy=_supply_apy_plf,
        borrow_apy=_borrow_apy_plf,
    )
    ### Supply and borrow rates are default 0.06 and 0.07 respectively, can be changed
    ### Collateral ratio is 1.2 by default, can be changed

    # assume that 80% of the supplied funds are borrowed
    market_maker.borrow_repay(initial_borrowed_funds, dai_plf)

    # create a user for the aggregator, has 10M DAI available
    aggregator = User(
        env=simulation_env,
        name="aggregator",
        funds_available={"dai": initial_supplied_funds_aggr},
    )
    # aggregator supplies all funds into the plf pool
    aggregator.supply_withdraw(initial_supplied_funds_aggr, dai_plf)

    # create array of x days of returns
    returns = [0.0] * days_to_simulate

    # simulate random walk for gov token price
    gov_token_prices = Randwalk(365, _startprice_governance_token, 0.05)

    # simulate every day
    for i in range(days_to_simulate):
        simulation_env.prices["aave"] = gov_token_prices[i]
        dai_plf.accrue_interest()
        dai_plf.distribute_reward(_gov_tokens_distributed_perday)
        returns[i] = aggregator.wealth

    return returns


returns_1 = simulate_simple_lending(1000, 500000000, 0.8, 0.007, 0.06, 0.08, 100, 365)
returns_2 = simulate_simple_lending(100, 500000000, 0.8, 0.007, 0.06, 0.08, 100, 365)
returns_3 = simulate_simple_lending(10, 500000000, 0.8, 0.007, 0.06, 0.08, 100, 365)
plt.plot(returns_1, label="Highest start price")
plt.plot(returns_2, label="Medium start price")
plt.plot(returns_3, label="Lowest start price")
plt.legend(loc="lower right")

# random walk for gov token price
