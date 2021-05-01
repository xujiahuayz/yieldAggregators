from os import name

from numpy import iterable
from yieldenv.amm import CPAmm
import logging
import matplotlib.pyplot as plt

# toggle between logging.INFO and logging.DEBUG for less or more prints
logging.basicConfig(level=logging.INFO)

"""
Storyline: investor had 100 DAI to invest,
and turned half of them to ETH for liquidity provision
"""


# traders only sell DAI to the pool
args1 = [(10, 0)] * 40


# traders only sell ETH to the pool
args2 = [(10, 1)] * 40


# traders alternatingly sell DAI and ETH to the pool
args3 = [(10, 0), (10, 1)] * 20


def plot_value_course(args, plot_title):
    # a pool with 50 DAI and 50 ETH, DAI is numeraire
    fee_level = 0.005
    pool = CPAmm(initial_reserves=[50, 50], fee=fee_level)
    volume_course_DAI = [0]
    fees = [0]
    pool_value = [pool.pool_value]
    for arg in args:
        pool.sell_to_pool(sell_quantity=arg[0], sell_index=arg[1])
        pool_value.append(pool.pool_value)
        volume_course_DAI.append(pool.volumes[0])
        fees.append(pool.volumes[0] * fee_level)

    plt.plot(pool_value)
    plt.title(plot_title)
    plt.xlabel("Pool value in DAI")
    plt.show()

    plt.plot(volume_course_DAI)
    plt.xlabel("Accumulated volume in DAI")
    plt.show()


if __name__ == "__main__":
    plot_value_course(args1, "sell DAI only")
    plot_value_course(args2, "sell ETH only")
    plot_value_course(args3, "alternating sell")
