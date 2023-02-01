from os import path
import matplotlib.pyplot as plt
import numpy as np

from yieldenv.settings import PROJECT_ROOT

RB_FACTOR = 25
RS_FACTOR = 50
# EXPONENT = 0.7


def borrow_lend_rates(
    util_rate: float,
    rb_factor: float = RB_FACTOR,
    rs_factor: float = RS_FACTOR,
) -> tuple[float, float]:
    """
    calculate borrow and supply rates based on utilization ratio
    with an arbitrarily-set shape
    """

    assert (
        0 <= util_rate < 1
    ), f"utilization ratio must lie in [0,1), but got {util_rate}"

    borrow_rate = util_rate / (rb_factor * (1 - util_rate))
    # initial_borrow_rate / (1 - util_rate) ** EXPONENT
    supply_rate = util_rate / (rs_factor * (1 - util_rate))
    # initial_supply_rate / (1 - util_rate) ** EXPONENT
    return borrow_rate, supply_rate


if __name__ == "__main__":
    # exploratory plot
    util_rates = np.concatenate(
        [np.arange(0, 0.83, step=0.02), np.arange(0.835, 0.9999, step=0.0001)]
    )

    borrow_rates = []
    lend_rates = []

    for u in util_rates:
        r1, r2 = borrow_lend_rates(u)
        borrow_rates.append(r1)
        lend_rates.append(r2)

    plt.rcParams.update({"font.size": 15})

    plt.plot(
        util_rates,
        borrow_rates,
        label=f"borrow interest rate $r_b=\\frac{{u}}{{{RB_FACTOR} \\times (1-u)}}$",
    )
    plt.plot(
        util_rates,
        lend_rates,
        label=f"supply interest rate $r_s=\\frac{{u}}{{{RS_FACTOR}  \\times (1-u)}}$",
    )
    plt.xlabel("utilization ratio $u$")
    plt.ylabel("interest rate per annum $r$")
    plt.xlim(0, 1)
    plt.ylim(0, 1.6)
    plt.legend(frameon=False)
    plt.tight_layout()
    fig_path = path.join(PROJECT_ROOT, f"assets/interest_model.pdf")
    plt.savefig(fig_path)
    plt.show()
    plt.close()
