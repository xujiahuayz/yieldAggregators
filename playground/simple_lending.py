from yieldenv.utils import PriceDict
from yieldenv.env import Env, User, Plf
import matplotlib.pyplot as plt
import numpy as np
from itertools import islice


def define_price_gov_token(days: int, _start_price: float, _trend_pct: float):

    y = _start_price
    price = [y]

    for _ in range(days):
        y = y * (1+_trend_pct)
        price.append(y)

    return price


def simulate_simple_lending(
    _startprice_governance_token: float,
    _initial_funds_plf: float,
    _initial_borrow_ratio: float,
    _aggregator_percentage_liquidity_plf: float,
    _supply_apy_plf: float,
    _borrow_apy_plf: float,
    _gov_tokens_distributed_perday: float,
    _gov_price_trend:float, 
    _days_to_simulate: int = 365,
):

    # initialization vars
    initial_supplied_funds_plf = _initial_funds_plf
    initial_borrowed_funds = _initial_borrow_ratio * initial_supplied_funds_plf
    initial_supplied_funds_aggr = (
        _aggregator_percentage_liquidity_plf * initial_supplied_funds_plf
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
    gov_token_prices = define_price_gov_token(days_to_simulate, _startprice_governance_token, _gov_price_trend)

    # simulate every day
    for i in range(days_to_simulate):
        simulation_env.prices["aave"] = gov_token_prices[i]
        dai_plf.accrue_interest()
        dai_plf.distribute_reward(_gov_tokens_distributed_perday)
        returns[i] = aggregator.wealth

    return returns



#--------------------- SIMULATING ------------------

dict = {}
for n in (10, 100, 1000): 
    for m in (0.05, 0.06, 0.07):

        x = str(n) + '_' + str(m)
        dict[x] = simulate_simple_lending(
            _startprice_governance_token = n,
            _initial_funds_plf = 500000000,
            _initial_borrow_ratio = 0.8,
            _aggregator_percentage_liquidity_plf = 0.007,
            _supply_apy_plf = m,
            _borrow_apy_plf = 0.08,
            _gov_tokens_distributed_perday = 100,
            _gov_price_trend =  0.002,
            _days_to_simulate =  365)

benchmark = simulate_simple_lending(
            _startprice_governance_token = 0,
            _initial_funds_plf = 500000000,
            _initial_borrow_ratio = 0.8,
            _aggregator_percentage_liquidity_plf = 0.007,
            _supply_apy_plf = 0,
            _borrow_apy_plf = 0.08,
            _gov_tokens_distributed_perday = 100,
            _gov_price_trend =  0.002,
            _days_to_simulate =  365)




#--------------------- PLOTTING ------------------

fontsize = 14
title_fontsize = 14

for item in islice(dict.items(), 0, 3):
    plt.plot(item[1], label = "APR " + item[0].split("_", 1)[1])
plt.plot(benchmark, label='benchmark')
plt.legend(loc='upper left', title="Start price " + item[0].split("_", 1)[0], fontsize = fontsize, title_fontsize = title_fontsize)
plt.show()
plt.close()

for item in islice(dict.items(), 3, 6):
    plt.plot(item[1], label = "APR " + item[0].split("_", 1)[1])
plt.plot(benchmark, label='benchmark')
plt.legend(loc='upper left', title="Start price " + item[0].split("_", 1)[0], fontsize = fontsize, title_fontsize = title_fontsize)
plt.show()
plt.close()

for item in islice(dict.items(), 6, 9):
    plt.plot(item[1], label = "APR " + item[0].split("_", 1)[1])
plt.plot(benchmark, label='benchmark')
plt.legend(loc='upper left', title="Start price " + item[0].split("_", 1)[0], fontsize = fontsize, title_fontsize = title_fontsize)
plt.show()
plt.close()

# for key, value in dict.items():
#     plt.plot(value, label = key)

# lines = plt.gca().get_lines()

# legend_1 = plt.legend([lines[i] for i in [0,1,2]], ['0.05 APY', '0.06 APY', '0.07 APY'], title = 'starting price 10', loc=2)
# legend_2 = plt.legend([lines[i] for i in [3,4,5]], ['0.05 APY', '0.06 APY', '0.07 APY'], title = 'starting price 100', loc = 6)
# legend_3 = plt.legend([lines[i] for i in [6,7,8]], ['0.05 APY', '0.06 APY', '0.07 APY'], title = 'starting price 1000', loc = 9)
# plt.gca().add_artist(legend_1)
# plt.gca().add_artist(legend_2)
# plt.show()


