from typing import Literal
from yieldenv.utils import simulation_plot

from yieldenv.strategies import (
    simulate_simple_lending,
    simulate_spiral_lending,
    simulate_cpamm,
)

N_ARRAY = [0, 1, 2]
DAYS_TO_SIMULATE = 365
GOV_TOKENS_DISTRIBUTED_PERDAY = 0.01
GOV_PRICE_TREND = 0.001
AGGREGATOR_POOL_PERCENTAGE = 0.01


# --------------------- SIMPLE LENDING ------------------
simulated_simple_lending = {
    str(n): {
        str(m): simulate_simple_lending(
            _startprice_governance_token=n,
            _initial_funds_plf=1 / AGGREGATOR_POOL_PERCENTAGE,
            _initial_borrow_ratio=0.8,
            _aggregator_percentage_liquidity_plf=AGGREGATOR_POOL_PERCENTAGE,
            _supply_apy_plf=m,
            _borrow_apy_plf=0.06,
            _gov_tokens_distributed_perday=GOV_TOKENS_DISTRIBUTED_PERDAY,
            _gov_price_trend=GOV_PRICE_TREND,
            _days_to_simulate=DAYS_TO_SIMULATE,
        )
        for m in (0, 0.03, 0.09)
    }
    for n in N_ARRAY
}

# --------------------- SPIRAL LENDING ------------------
simulated_spiral_lending = {
    str(n): {
        str(m): simulate_spiral_lending(
            _startprice_governance_token=n,
            _initial_funds_plf=1 / AGGREGATOR_POOL_PERCENTAGE,
            _initial_borrow_ratio=0.8,
            _aggregator_percentage_liquidity_plf=AGGREGATOR_POOL_PERCENTAGE,
            _supply_apy_plf=0.03,
            _borrow_apy_plf=0.06,
            _gov_tokens_distributed_perday=GOV_TOKENS_DISTRIBUTED_PERDAY,
            _gov_price_trend=GOV_PRICE_TREND,
            _spirals=m,
            _days_to_simulate=DAYS_TO_SIMULATE,
        )
        for m in (0, 2, 8)
    }
    for n in N_ARRAY
}

# --------------------- AMM LP ------------------

startprice_quote_token = 10
initial_supplied_funds_amm = {
    "dai": 1 / AGGREGATOR_POOL_PERCENTAGE / 2,
    "eth": 1 / AGGREGATOR_POOL_PERCENTAGE / startprice_quote_token / 2,
}


simulated_cpamm = {
    str(n): {
        m: simulate_cpamm(
            _initial_supplied_funds_amm=initial_supplied_funds_amm.copy(),
            _startprice_quote_token=startprice_quote_token,
            _percentage_liquidity_aggr=AGGREGATOR_POOL_PERCENTAGE,
            _startprice_governance_token=n,
            _gov_tokens_distributed_perday=GOV_TOKENS_DISTRIBUTED_PERDAY,
            _pct_of_pool_to_trade=m,
            _gov_price_trend=GOV_PRICE_TREND,
            _days_to_simulate=DAYS_TO_SIMULATE,
            # _scenario=m,
            _fee=0.05,
        )
        for m in [
            (0, 0),
            (0.4, 0.6),
            (0.5, 0.5),
            (0.6, 0.4),
        ]
    }
    for n in N_ARRAY
}

# --------------------- PLOTTING ------------------

simulation_plot(
    simulated_data=simulated_simple_lending, legend_title="annualized return"
)
simulation_plot(
    simulated_data=simulated_spiral_lending, legend_title="number of spirals"
)
simulation_plot(simulated_data=simulated_cpamm, legend_title="volume (buy, sell)")
