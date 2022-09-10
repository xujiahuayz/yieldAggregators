from collections.abc import MutableMapping
from yieldenv.settings import PROJECT_ROOT
import matplotlib.pyplot as plt
from typing import Optional, Literal
from os import path

from yieldenv.constants import INTEREST_TOKEN_PREFIX, DEBT_TOKEN_PREFIX


class PriceDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.__dict__ = dict()

        # calls newly written `__setitem__` below
        self.update(*args, **kwargs)

    # The next five methods are requirements of the ABC.
    def __setitem__(self, key: str, value: float):
        if INTEREST_TOKEN_PREFIX in key or DEBT_TOKEN_PREFIX in key:
            raise ValueError("can only set underlying price")
        self.__dict__[key] = value
        self.__dict__[INTEREST_TOKEN_PREFIX + key] = value
        self.__dict__[DEBT_TOKEN_PREFIX + key] = -value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        """returns simple dict representation of the mapping"""
        return str(self.__dict__)

    def __repr__(self):
        """echoes class, id, & reproducible representation in the REPL"""
        return f"{self.__dict__}"


def define_price_gov_token(days: int, _start_price: float, _trend_pct: float):

    y = _start_price
    price = [y]

    for _ in range(days):
        y = y * (1 + _trend_pct)
        price.append(y)

    return price


def simulation_plot(
    file_name: str,
    simulated_data: dict[str, dict[str, list[float]]],
    legend_title: str,
    legend_loc: str = "upper left",
    xlabel_text: str = "day $t$",
    ylabel_text: str = "yield farming pool value $W_t$",
    ticks_fontsize: float = 22,
    ylim_lower: float = 0.85,
    ylim_upper: float = 1.45,
    axes_fontsize: float = 23,
    legend_title_fontsize: float = 21,
    title_fontsize: float = 23,
    legend_fontsize: float = 21,
    plot_title_prefix: Optional[str] = "reward token price",
    plot_title_loc: Literal["center", "left", "right"] = "center",
):
    for n, series in simulated_data.items():
        for key, value in series.items():
            plt.plot(value, label=key)
        plt.xlabel(xlabel=xlabel_text, fontsize=axes_fontsize)
        plt.ylabel(ylabel=ylabel_text, fontsize=axes_fontsize)
        plt.xticks(fontsize=ticks_fontsize)
        plt.yticks(fontsize=ticks_fontsize)
        plt.ylim(ylim_lower, ylim_upper)
        plt.legend(
            loc=legend_loc,
            title=legend_title,
            fontsize=legend_fontsize,
            title_fontsize=legend_title_fontsize,
            labelspacing=0.1,
            frameon=False,
        )
        if plot_title_prefix:
            label = f"{plot_title_prefix}: ${n} \\, \\tt{{ USDT}}$"
            plt.title(label=label, loc=plot_title_loc, fontsize=title_fontsize)
        plt.tight_layout()
        fig_path = path.join(PROJECT_ROOT, f"assets/{n}_{file_name}.pdf")
        plt.savefig(fig_path)
        plt.show()
        plt.close()
