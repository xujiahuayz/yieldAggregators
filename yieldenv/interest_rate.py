from cProfile import label
import matplotlib.pyplot as plt
import numpy as np


def borrow_lend_rates(util_rate: float) -> tuple[float, float]:
    borrow_rate = 0.03 / (1 - util_rate) ** 0.7
    lend_rate = 0.01 / (1 - util_rate) ** 0.7
    return borrow_rate, lend_rate


if __name__ == "__main__":
    # exploratory plot
    util_rates = np.concatenate(
        [np.arange(0, 0.8, step=0.1), np.arange(0.81, 0.9999, step=0.0001)]
    )

    borrow_rates = []
    lend_rates = []

    for u in util_rates:
        r1, r2 = borrow_lend_rates(u)
        borrow_rates.append(r1)
        lend_rates.append(r2)

    plt.plot(util_rates, borrow_rates, label="Borrow rate")
    plt.plot(util_rates, lend_rates, label="Supply rate")
    plt.xlabel("Utilization ratio")
    plt.ylabel("Interest rate p.a.")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend()
