import logging
from os import name
from yieldenv.env import CPAmm, Env, User, Plf
import matplotlib.pyplot as plt

# toggle between logging.INFO and logging.DEBUG for less or more prints
logging.basicConfig(level=logging.INFO)


simulation_env = Env(prices={"dai": 1, "eth": 1, "i-dai": 1, "b-dai": 1})
simulation_env.prices["aave"] = 10
alice = User(env=simulation_env, name="alice", funds_available={"dai": 6000})
print(alice.funds_available, "alice")
bob = User(env=simulation_env, name="bob", funds_available={"dai": 12000})
print(bob.funds_available, "bob")

dai_plf = Plf(env=simulation_env, reward_token_name="aave", initiator=alice)
print(alice.funds_available, "alice")

alice.supply_withdraw(1200, dai_plf)
print(alice.funds_available, "alice")
bob.supply_withdraw(600, dai_plf)
print(bob.funds_available, "bob")
alice.supply_withdraw(-500, dai_plf)
print(alice.funds_available, "alice")

alice.borrow_repay(100, dai_plf)
print(alice.funds_available, "alice")

dai_plf.distribute_reward(200)
print(alice.funds_available, "alice")
print(bob.funds_available, "bob")

dai_plf.accrue_interest()
print(alice.funds_available, "alice")
print(bob.funds_available, "bob")

print(alice.wealth)

"""
Storyline: investor had 100 DAI to invest,
and turned half of them to ETH for liquidity provision
"""


simulation_env = Env(prices={"dai": 1, "eth": 2})
alice = User(env=simulation_env, name="alice", funds_available={"dai": 1000, "eth": 50})
alice.wealth

dai_eth_amm = CPAmm(
    env=simulation_env,
    reward_token_name="aave",
    fee=0.003,
    initiator=alice,
    initial_reserves=[20, 20],
)


alice.update_liquidity(pool_shares_delta=0.2, amm=dai_eth_amm)
alice.wealth


bob = User(env=simulation_env, name="bob", funds_available={"dai": 1000, "eth": 500})
# bob sells 10 eth
bob.sell_to_amm(dai_eth_amm, sell_quantity=10, sell_index=1)

bob.wealth

alice.wealth
alice.funds_available

charlie = User(
    env=simulation_env, name="charlie", funds_available={"dai": 30, "eth": 90}
)
charlie.sell_to_amm(dai_eth_amm, sell_quantity=3, sell_index=0)
charlie.funds_available

charlie.update_liquidity(0.1, amm=dai_eth_amm)
charlie.funds_available

alice.funds_available
alice.wealth

dai_eth_amm.distribute_reward(quantity=50)
alice.funds_available
charlie.funds_available
alice.wealth
simulation_env.prices["aave"] = 10
alice.wealth

# dai_eth_amm
# # traders only sell DAI to the pool
# args1 = [(10, 0)] * 40


# # traders only sell ETH to the pool
# args2 = [(10, 1)] * 40


# # traders alternatingly sell DAI and ETH to the pool
# args3 = [(10, 0), (10, 1)] * 20


# def plot_value_course(args, plot_title):
#     # a pool with 50 DAI and 50 ETH, DAI is numeraire
#     fee_level = 0.005
#     pool = CPAmm(initial_reserves=[50, 50], fee=fee_level)
#     volume_course_DAI = [0]
#     fees = [0]
#     pool_value = [pool.pool_value]
#     for arg in args:
#         pool.sell_to_pool(sell_quantity=arg[0], sell_index=arg[1])
#         pool_value.append(pool.pool_value)
#         volume_course_DAI.append(pool.volumes[0])
#         fees.append(pool.volumes[0] * fee_level)

#     plt.plot(pool_value)
#     plt.title(plot_title)
#     plt.xlabel("Pool value in DAI")
#     plt.show()

#     plt.plot(volume_course_DAI)
#     plt.xlabel("Accumulated volume in DAI")
#     plt.show()


# if __name__ == "__main__":
#     plot_value_course(args1, "sell DAI only")
#     plot_value_course(args2, "sell ETH only")
#     plot_value_course(args3, "alternating sell")
