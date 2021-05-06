# make sure User is recognized
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
import logging
from typing import Dict, Optional, cast


@dataclass
class Env:
    users: Dict[str, User] = field(default_factory=dict)
    prices: Dict[str, float] = field(default_factory=lambda: {"dai": 1.0, "eth": 1.0})


class User:
    def __init__(self, env: Env, name: str, funds_available: Optional[dict] = None):
        assert name not in env.users, f"User {name} exists"
        self.env = env
        # add the user to the environment
        self.env.users[name] = self

        if funds_available is None:
            funds_available = {"dai": 0.0, "eth": 0.0}
        self.funds_available = funds_available
        self.env = env

        self.collected_tokens = 0.0
        self.deposit = 0.0
        self.borrowed_funds = 0.0  # keep track of user borrowed funds
        self.name = name

    @property
    def wealth(self) -> float:
        user_wealth = sum(
            value * self.env.prices[asset_name]
            for asset_name, value in self.funds_available.items()
        )
        logging.info(f"{self.name}'s wealth in DAI: {user_wealth}")

        return user_wealth

    # # AMM actions
    # def initiate_amm(
    #     self, reward_token_name, initial_reserves, fee, asset_names
    # ) -> CPAmm:

    #     CPAmm(
    #         env=self.env,
    #         reward_token_name=reward_token_name,
    #         initial_reserves=initial_reserves,
    #         fee=fee,
    #         asset_names=asset_names,
    #     )

    def sell_to_amm(self, amm: CPAmm, sell_quantity: float, sell_index: int = 0):
        """
        `quantity` means how much quantity to sell (add) to the pool;
        index means which asset it is
        """

        # initialize asset balance if not yet there
        for w in amm.asset_names:
            if w not in self.funds_available:
                self.funds_available[w] = 0.0

        assert sell_quantity >= 0, "must sell a non-negative quantity"
        assert sell_index in [0, 1], "reserve_index out of range"

        assert (
            self.funds_available[amm.asset_names[sell_index]] >= sell_quantity
        ), "insufficient funds to sell"

        old_invariant = amm.invariant

        # deduct sold quantity from user's funds
        self.funds_available[amm.asset_names[sell_index]] -= sell_quantity

        # add sold quantity to the reserve with `reserve_index`
        amm.reserves[sell_index] += sell_quantity
        amm.volumes[sell_index] += sell_quantity

        # theoretical new quantity of the other reserve
        _new_reserve = old_invariant / amm.reserves[sell_index]
        buy_index = 1 - sell_index
        # theoretical quantity purchased

        buy_quantity = amm.reserves[buy_index] - _new_reserve

        # keep a record of the volume on the buy side
        amm.volumes[buy_index] += buy_quantity

        # fee charge
        swap_fee = buy_quantity * amm.fee
        # add fee to revenue
        amm.fee_retained_by_reserve[buy_index] += swap_fee

        # actual quantity the trader gets
        buy_quantity -= swap_fee

        # add buy quantity to user's funds
        self.funds_available[amm.asset_names[buy_index]] += buy_quantity

        # update actual new quantity of the buy reserve
        amm.reserves[buy_index] -= buy_quantity

        # update market price due to trading
        self.env.prices[amm.asset_names[1]] = amm.spot_price

        logging.debug(
            f"""
            old invariant: {old_invariant}
            Sell {sell_quantity} in asset#{sell_index}, get {buy_quantity} in asset#{buy_index},
            Earned fee: {swap_fee} in asset#{buy_index}
            new invariant: {amm.invariant}
            """
        )

    def update_liquidity(self, pool_shares_delta: float, amm: CPAmm):

        """
        add (pool_shares_delta>0) or remove (pool_shares_delta<0) liquidity to an AMM
        """

        if self.name not in amm.user_pool_shares:
            amm.user_pool_shares[self.name] = 0

        assert (
            amm.user_pool_shares[self.name] + pool_shares_delta >= 0
        ), "cannot deplete user pool shares"

        # with signs, + means add to pool. - means remove from pool
        liquidity_fraction_delta = pool_shares_delta / amm.total_pool_shares
        funds_delta = [w * liquidity_fraction_delta for w in amm.reserves]

        assert all(
            self.funds_available[amm.asset_names[i]] - funds_delta[i] >= 0
            for i in range(2)
        ), "insufficient funds to provide liquidity"

        for i in range(2):
            # update own funds
            self.funds_available[amm.asset_names[i]] -= funds_delta[i]
            # update liquidity pool
            amm.reserves[i] += funds_delta[i]

        # update pool shares of the user in the pool registry
        amm.user_pool_shares[self.name] += pool_shares_delta

        # matching balance in user's account to pool registry record
        self.funds_available[amm.lp_token_name] = amm.user_pool_shares[self.name]

    # PLF actions ----
    def supply(self, amount: float, plf: Plf):
        plf.process_supply(amount)
        self.deposit += amount

        # self.deposit_available_as_collateral += amount

    def withdraw(self, amount: float, plf: Plf):
        plf.process_withdraw(amount)
        self.deposit -= amount
        # self.deposit_available_as_collateral -= amount

    def deposit_available_as_collateral(self, plf: Plf) -> float:
        return self.deposit - self.borrowed_funds * plf.collateral_ratio

    def borrow(self, amount: float, plf: Plf):
        minimum_deposit_available_needed = amount * plf.collateral_ratio
        assert (
            self.deposit_available_as_collateral(plf=plf)
            >= minimum_deposit_available_needed
        ), "Borrow position under-collateralized"
        plf.process_borrow(amount)
        self.borrowed_funds += amount

    def repay(self, amount: float, plf: Plf):  # = paying back loan
        plf.process_repay(amount)
        self.borrowed_funds -= amount

    def net_interest_profit(self, plf: Plf):
        daily_interest_revenue = self.deposit * (plf.supply_apr / 365)
        daily_interest_cost = self.borrowed_funds * np.exp(plf.borrow_apr / 365)
        return daily_interest_revenue - daily_interest_cost

    def plf_reward_tokens_value(self, token_price: float, plf: Plf) -> float:
        # Governance token distribution ---
        tokens_for_supplying = (
            (self.deposit / plf.total_available_funds) * plf.distribution_per_day * 0.5
        )  # 50% goes to suppliers
        tokens_for_borrowing = (
            (self.borrowed_funds / plf.total_borrowed_funds)
            * plf.distribution_per_day
            * 0.5
        )  # 50% goes to borrowers
        reward_tokens = tokens_for_supplying + tokens_for_borrowing

        return reward_tokens * token_price

    def plf_yield(self, token_price: float, plf: Plf) -> float:
        return self.net_interest_profit(plf=plf) + self.plf_reward_tokens_value(
            token_price=token_price, plf=plf
        )


@dataclass
class CPAmm:
    """
    reserves[0] is the numeraire
    fee represents the fraction of **output asset** that got retained within the pool
    """

    env: Env
    reward_token_name: str
    initiator: User
    initial_reserves: list[float] = field(default_factory=lambda: [50.0, 50.0])
    fee: float = 0.005
    asset_names: list[str] = field(default_factory=lambda: ["dai", "eth"])

    def __post_init__(self):
        lp_token_name = "-".join(self.asset_names) + "-lp"
        self.lp_token_name = lp_token_name

        available_prices = self.env.prices
        if lp_token_name in available_prices and available_prices[lp_token_name] != 0:
            raise RuntimeError(
                "an amm pool with the same token pair exists. cannot create new one."
            )

        assert all(
            w > 0 for w in self.initial_reserves
        ), "must provide positive liquidity on both sides"

        assert all(
            self.asset_names[i] in self.initiator.funds_available
            and self.initiator.funds_available[self.asset_names[i]]
            >= self.initial_reserves[i]
            for i in range(2)
        ), "insufficient funds"

        # deduct funds from user balance
        for i in range(2):
            self.initiator.funds_available[
                self.asset_names[i]
            ] -= self.initial_reserves[i]

        self.reserves = self.initial_reserves

        initial_pool_share = 1.0
        self.user_pool_shares = {self.initiator.name: initial_pool_share}

        # add LP token into initiator's wallet
        self.initiator.funds_available[lp_token_name] = initial_pool_share

        # update 'eth' market price as implied by pool composition
        available_prices[self.asset_names[1]] = self.spot_price

        # update LP token and reward token price immediately
        available_prices[lp_token_name] = self.lp_token_price

        # if reward token is a new token, then initiate price with 0
        reward_token_name = self.reward_token_name
        if reward_token_name not in available_prices:
            available_prices[self.reward_token_name] = 0

        # initalize volume and fee bookkeeping
        self.volumes = [0.0, 0.0]
        self.fee_retained_by_reserve = [0.0, 0.0]

    @property
    def total_pool_shares(self) -> float:
        return sum(self.user_pool_shares.values())

    @property
    def invariant(self) -> float:
        return cast(float, np.prod(self.reserves))

    @property
    def spot_price(self) -> float:
        return self.reserves[0] / self.reserves[1]

    @property
    def pool_value(self) -> float:
        return self.reserves[0] * 2

    @property
    def lp_token_price(self) -> float:
        if self.total_pool_shares == 0:
            return 0.0
        return self.pool_value / self.total_pool_shares

    # # this does not make sense any more if we allow liquidity addition
    # @property
    # def value_held(self):
    #     return self.initial_reserves[0] + self.initial_reserves[1] * self.spot_price

    def __repr__(self):
        return f"(reserves={self.reserves},invariant={self.invariant})"

    def get_user_pool_fraction(self, user_name: str) -> float:
        if user_name not in self.user_pool_shares:
            self.user_pool_shares[user_name] = 0.0
        return self.user_pool_shares[user_name] / self.total_pool_shares

    def distribute_reward(self, quantity: float):
        for user_name in self.user_pool_shares:
            user_funds = self.env.users[user_name].funds_available

            # initialize if the balance does not exist before airdropping
            if self.reward_token_name not in user_funds:
                user_funds[self.reward_token_name] = 0

            # distribute reward token proportionaly
            user_funds[self.reward_token_name] += (
                self.get_user_pool_fraction(user_name=user_name) * quantity
            )


class Plf:
    def __init__(
        self,
        supply_apr: float,
        borrow_apr: float,
        distribution_per_day: float,
        initial_starting_funds: float = 1000,
        collateral_ratio: float = 1.2,
    ):
        self.supply_apr = supply_apr
        self.borrow_apr = borrow_apr
        self.total_available_funds = initial_starting_funds
        self.total_borrowed_funds = 0.5 * initial_starting_funds
        self.collateral_ratio = (
            collateral_ratio
            # collateral divided by amount able to borrow
        )
        self.distribution_per_day = distribution_per_day

    def setSupplyApr(self, apr: float):
        self.supply_apr = apr

    def setBorrowApr(self, apr: float):
        self.borrow_apr = apr

    def process_supply(self, amount):
        self.total_available_funds += amount

    def process_withdraw(self, amount):
        self.total_available_funds -= amount

    def process_borrow(self, amount: float):
        assert (
            self.total_available_funds + amount
        ) <= self.total_available_funds, "Lending pool cannot be depleted"
        self.total_borrowed_funds += amount

    def process_repay(self, amount: float):  # = paying back loan
        self.total_borrowed_funds -= amount
