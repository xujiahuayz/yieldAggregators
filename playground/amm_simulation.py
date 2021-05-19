from yieldenv.env import Env, PriceDict, User, CPAmm
import matplotlib.pyplot as plt
import numpy as np
import random
from operator import add
from itertools import islice


"""
Storyline: investor provides LP tokens to a yield aggregator, which 
accrues yield by collecting trading fees + yield of a liquidity mining program +
potential loss through divergence loss
"""


def define_price_gov_token(days: int, _start_price: float, _trend_pct: float):

    y = _start_price
    price = [y]

    for _ in range(days):
        y = y * (1+_trend_pct)
        price.append(y)

    return price


def simulate_cpamm(
    _initial_supplied_funds_amm: dict,
    _startprice_quote_token: float,
    _percentage_liquidity_aggr: float,
    _startprice_governance_token: float,
    _gov_tokens_distributed_perday: float,
    _pct_of_pool_to_trade: float,
    _gov_price_trend:float, 
    _initial_funds_trader: dict = {"dai": 1e20, "eth": 1e20},
    _days_to_simulate: int = 365,
    _scenario: str = "no trades",
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
        fee=0.003,
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

    #set daily traded volume
    daily_traded_volume = _pct_of_pool_to_trade * dai_eth_amm.pool_value / _days_to_simulate

    # simulate random walk for gov token price
    gov_token_prices = define_price_gov_token(_days_to_simulate, _startprice_governance_token, _gov_price_trend)

    # simulate every day
    if _scenario == "no trades":
        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)

            returns[i] = aggregator.wealth
    elif _scenario == "only buy":
        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            for m in range(50):
                trade_amount = random.uniform(0, daily_traded_volume)
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=0)

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)

            returns[i] = aggregator.wealth
    elif _scenario == "only sell":
        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            for m in range(50):
                trade_amount = random.uniform(0, daily_traded_volume / simulation_env.prices['eth']) #divide by price of ETH when selling ETH
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=1)

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)


            returns[i] = aggregator.wealth
    elif _scenario == "both":

        for i in range(_days_to_simulate):
            simulation_env.prices["sushi"] = gov_token_prices[i]

            for m in range(25):
                trade_amount = random.uniform(0, daily_traded_volume)
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=0)
                trade_amount = random.uniform(0, daily_traded_volume / simulation_env.prices['eth']) #divide by price of ETH when selling ETH
                trader.sell_to_amm(dai_eth_amm, trade_amount, sell_index=1)

            dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)


            returns[i] = aggregator.wealth
    else:
        print("Scenario not available")
        returns = None

    return returns



#--------------------- SIMULATING ------------------

startprice_quote_token= 100
percentage_liquidity_aggr=0.01
initial_supplied_funds_amm = {"dai": 1/percentage_liquidity_aggr/2, "eth": 1/percentage_liquidity_aggr/startprice_quote_token/2}
gov_tokens_distributed_perday = 0.01
gov_price_trend = 0.002
pct_of_pool_to_trade = 0.005
days_to_simulate=365


dict = {}
for n in (0, 2, 5): 
    for m in ('no trades',
      'only buy',
      'only sell',
       'both'
       ):

        x = str(n) + '_' + str(m)
        dict[x] = simulate_cpamm(
            _initial_supplied_funds_amm=initial_supplied_funds_amm.copy(),
            _startprice_quote_token=startprice_quote_token,
            _percentage_liquidity_aggr=percentage_liquidity_aggr,
            _startprice_governance_token = n,
            _gov_tokens_distributed_perday=gov_tokens_distributed_perday,
            _pct_of_pool_to_trade = pct_of_pool_to_trade,
            _gov_price_trend = gov_price_trend,
            _days_to_simulate=days_to_simulate,
            _scenario = m,
            )



#--------------------- PLOTTING ------------------

fontsize = 14
title_fontsize = 14
axes_fontsize = 14
ticks_fontsize = 14
ylim_lower = 0.7
ylim_upper= 1.5

for item in islice(dict.items(), 0, 4):
    plt.plot(item[1], label = "APR " + item[0].split("_", 1)[1])
plt.xlabel("Day", fontsize = axes_fontsize)
plt.ylabel("Wealth (DAI)", fontsize = axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.ylim(ylim_lower, ylim_upper)
plt.legend(loc='lower right', title="Start price " + item[0].split("_", 1)[0], fontsize = fontsize, title_fontsize = title_fontsize)
plt.show()
plt.close()

for item in islice(dict.items(), 4, 8):
    plt.plot(item[1], label = "APR " + item[0].split("_", 1)[1])
plt.xlabel("Day", fontsize = axes_fontsize)
plt.ylabel("Wealth (DAI)", fontsize = axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.ylim(ylim_lower, ylim_upper)
plt.legend(loc='lower right', title="Start price " + item[0].split("_", 1)[0], fontsize = fontsize, title_fontsize = title_fontsize)
plt.show()
plt.close()

for item in islice(dict.items(), 8, 12):
    plt.plot(item[1], label = "APR " + item[0].split("_", 1)[1])
plt.xlabel("Day", fontsize = axes_fontsize)
plt.ylabel("Wealth (DAI)", fontsize = axes_fontsize)
plt.xticks(fontsize=ticks_fontsize)
plt.yticks(fontsize=ticks_fontsize)
plt.ylim(ylim_lower, ylim_upper)
plt.legend(loc='lower right', title="Start price " + item[0].split("_", 1)[0], fontsize = fontsize, title_fontsize = title_fontsize)
plt.show()
plt.close()

