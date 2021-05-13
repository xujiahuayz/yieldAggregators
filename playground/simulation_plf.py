import logging
from os import name
from yieldenv.env import CPAmm, Env, User, Plf
import matplotlib.pyplot as plt

# initialization vars
price_governance_token = 10
initial_supplied_funds_plf = 500000000
initial_borrowed_funds = 0.8 * initial_supplied_funds_plf
days_to_simulate = 365

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
)
### Supply and borrow rates are default 0.06 and 0.07 respectively, can be changed
### Collateral ratio is 1.2 by default, can be changed

# assume that 80% of the supplied funds are borrowed
market_maker.borrow_repay(initial_borrowed_funds, dai_plf)


# create a user for the aggregator, has 10M DAI available
aggregator = User(
    env=simulation_env, name="aggregator", funds_available={"dai": 10000000}
)
# aggregator supplies all funds into the plf pool
aggregator.supply_withdraw(10000000, dai_plf)


# create array of 100 days of returns
returns = [0] * days_to_simulate


# simulate every day

for i in range(days_to_simulate):
    dai_plf.receive_pay_interest()
    dai_plf.distribute_reward(100)
    returns[i] = aggregator.wealth


# TO DO ?:
# - Incoming and outgoing funds for aggregator
# - fluctuating prices of governance token
