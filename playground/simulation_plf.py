import logging
from os import name
from yieldenv.env import CPAmm, Env, User, Plf
import matplotlib.pyplot as plt


def simulate(
    _price_governance_token: float,
    _initial_funds_plf: float,
    _initial_borrow_ratio: float,
    _aggregator_percentage_liquidyt_plf: float,
    _supply_apy_plf: float,
    _borrow_apy_plf: float,
    _gov_tokens_distributed_perday: float,
    _days_to_simulate: int = 365,
):

    # initialization vars
    price_governance_token = _price_governance_token
    initial_supplied_funds_plf = _initial_funds_plf
    initial_borrowed_funds = _initial_borrow_ratio * initial_supplied_funds_plf
    initial_supplied_funds_aggr = (
        _aggregator_percentage_liquidyt_plf * initial_supplied_funds_plf
    )
    days_to_simulate = _days_to_simulate

    # set up an environment with all DAI prices of 1, price for governance token
    simulation_env = Env(prices={"dai": 1, "i-dai": 1, "b-dai": 1})
    simulation_env.prices["aave"] = price_governance_token

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
    returns = [0] * days_to_simulate

    # simulate every day

    for i in range(days_to_simulate):
        dai_plf.accrue_interest()
        dai_plf.distribute_reward(_gov_tokens_distributed_perday)
        returns[i] = aggregator.wealth

    return returns


returns = simulate(10, 500000000, 0.8, 0.007, 0.06, 0.08, 100, 365)
returns
