from typing import Literal
from yieldenv.utils import PriceDict, define_price_gov_token
from yieldenv.env import Env, User, Plf, CPAmm


def simulate_simple_lending(
    _startprice_governance_token: float,
    _initial_funds_plf: float,
    _initial_borrow_ratio: float,
    _aggregator_percentage_liquidity_plf: float,
    _supply_apy_plf: float,
    _borrow_apy_plf: float,
    _gov_tokens_distributed_perday: float,
    _gov_price_trend: float,
    _days_to_simulate: int = 365,
) -> list[float]:

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
    gov_token_prices = define_price_gov_token(
        days_to_simulate, _startprice_governance_token, _gov_price_trend
    )

    # simulate every day
    for i in range(days_to_simulate):
        simulation_env.prices["aave"] = gov_token_prices[i]
        dai_plf.accrue_interest()
        dai_plf.distribute_reward(_gov_tokens_distributed_perday)
        returns[i] = aggregator.wealth

    return returns


def simulate_spiral_lending(
    _startprice_governance_token: float,
    _initial_funds_plf: float,
    _initial_borrow_ratio: float,
    _aggregator_percentage_liquidity_plf: float,
    _supply_apy_plf: float,
    _borrow_apy_plf: float,
    _gov_tokens_distributed_perday: float,
    _gov_price_trend: float,
    _spirals: int,
    _days_to_simulate: int = 365,
) -> list[float]:

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
    aggregator.supply_withdraw(aggregator.funds_available["dai"], dai_plf)

    for i in range(_spirals):
        # print(aggregator.funds_available)

        amount_i_dai = aggregator.funds_available[dai_plf.interest_token_name]
        if dai_plf.borrow_token_name in aggregator.funds_available:
            amount_b_dai = aggregator.funds_available[dai_plf.borrow_token_name]
        else:
            amount_b_dai = 0

        available_to_borrow = (
            amount_i_dai / dai_plf.collateral_ratio - amount_b_dai - 0.1
        )

        # print(available_to_borrow)

        # aggregator puts borrowed funds back into plf
        aggregator.borrow_repay(available_to_borrow, dai_plf)

        # print(aggregator.funds_available)

        aggregator.supply_withdraw(available_to_borrow, dai_plf)

        # print(aggregator.funds_available)

    # create array of x days of returns
    returns = [0.0] * days_to_simulate

    # simulate random walk for gov token price
    gov_token_prices = define_price_gov_token(
        days_to_simulate, _startprice_governance_token, _gov_price_trend
    )

    # simulate every day
    for i in range(days_to_simulate):
        simulation_env.prices["aave"] = gov_token_prices[i]
        dai_plf.accrue_interest()
        dai_plf.distribute_reward(_gov_tokens_distributed_perday)
        returns[i] = aggregator.wealth

    return returns


def simulate_cpamm(
    _initial_supplied_funds_amm: dict,
    _startprice_quote_token: float,
    _percentage_liquidity_aggr: float,
    _startprice_governance_token: float,
    _gov_tokens_distributed_perday: float,
    _pct_of_pool_to_trade: float,
    _gov_price_trend: float,
    _initial_funds_trader: dict = {"dai": 1e20, "eth": 1e20},
    _days_to_simulate: int = 365,
    _scenario: Literal["no trades", "only buy", "only sell", "both"] = "no trades",
    _fee: float = 0.03,
) -> list[float]:
    """
    Storyline: investor provides LP tokens to a yield aggregator, which
    accrues yield by collecting trading fees + yield of a liquidity mining program +
    potential loss through divergence loss
    """

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
        fee=_fee,
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

    # set daily traded volume
    daily_traded_volume = (
        _pct_of_pool_to_trade * dai_eth_amm.pool_value / _days_to_simulate
    )

    # simulate random walk for gov token price
    gov_token_prices = define_price_gov_token(
        _days_to_simulate, _startprice_governance_token, _gov_price_trend
    )

    # simulate every day
    for i in range(_days_to_simulate):
        simulation_env.prices["sushi"] = gov_token_prices[i]
        dai_eth_amm.distribute_reward(quantity=_gov_tokens_distributed_perday)

        if _scenario == "only buy":
            trader.sell_to_amm(dai_eth_amm, daily_traded_volume, sell_index=0)
        elif _scenario == "only sell":
            trader.sell_to_amm(
                dai_eth_amm,
                daily_traded_volume / simulation_env.prices["eth"],
                sell_index=1,
            )
        elif _scenario == "both":
            trader.sell_to_amm(dai_eth_amm, daily_traded_volume / 2, sell_index=0)

            trader.sell_to_amm(
                dai_eth_amm,
                daily_traded_volume / simulation_env.prices["eth"] / 2,
                sell_index=1,
            )
        elif _scenario != "no trades":
            raise ValueError("Scenario not available")

        returns[i] = aggregator.wealth

    return returns
