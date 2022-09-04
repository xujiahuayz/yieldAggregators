# make sure User is recognized
from __future__ import annotations
from dataclasses import dataclass, field
from yieldenv.constants import DEBT_TOKEN_PREFIX, INTEREST_TOKEN_PREFIX
import numpy as np
import logging
from typing import Optional, cast
from yieldenv.interest_rate import borrow_lend_rates

from yieldenv.utils import PriceDict


class Env:
    def __init__(
        self,
        users: Optional[dict[str, User]] = None,
        prices: Optional[PriceDict] = None,
    ):
        if users is None:
            users = {}

        if prices is None:
            prices = PriceDict({"dai": 1.0, "eth": 2.0})

        self.users = users
        self.prices = prices

    @property
    def prices(self) -> PriceDict:
        return self._prices

    @prices.setter
    def prices(self, value: PriceDict):
        if type(value) is not PriceDict:
            raise TypeError("must use PriceDict type")
        self._prices = value


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

        self.name = name

    @property
    def wealth(self) -> float:

        user_wealth = sum(
            value * self.env.prices[asset_name]
            for asset_name, value in self.funds_available.items()
        )
        logging.info(f"{self.name}'s wealth in DAI: {user_wealth}")

        return user_wealth

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

        self.env.prices[amm.lp_token_name] = amm.lp_token_price

        logging.debug(
            f"""
            old invariant: {old_invariant}
            Sell {sell_quantity} in asset#{sell_index}, get {buy_quantity} in asset#{buy_index},
            Earned fee: {swap_fee} in asset#{buy_index}
            new invariant: {amm.invariant}
            """
        )

    def buy_from_amm(self, amm: CPAmm, buy_quantity: float, buy_index: int = 0):
        """
        `quantity` means how much quantity to buy (deduct) from the pool;
        index means which asset it is
        """

        # initialize asset balance if not yet there
        for w in amm.asset_names:
            if w not in self.funds_available:
                self.funds_available[w] = 0.0

        if buy_quantity < 0:
            raise ValueError("must buy a non-negative quantity")
        if buy_index not in [0, 1]:
            raise ValueError("reserve_index out of range")

        # need to pay for more than wanted, for fees
        actual_buy_quantity = buy_quantity / (1 - amm.fee)

        new_reserve_buy = amm.reserves[buy_index] - actual_buy_quantity

        if new_reserve_buy < 0:
            raise ValueError("Insufficient funds in the pool")

        sell_index = 1 - buy_index

        sell_quantity = amm.invariant / new_reserve_buy - amm.reserves[sell_index]

        self.sell_to_amm(amm=amm, sell_quantity=sell_quantity, sell_index=sell_index)

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

    # -------------------------  PLF actions ------------------------------

    def supply_withdraw(self, amount: float, plf: Plf):  # negative for withdrawing

        if self.name not in plf.user_i_tokens:
            plf.user_i_tokens[self.name] = 0

        assert (
            plf.user_i_tokens[self.name] + amount >= 0
        ), "cannot withdraw more i-tokens than you have"

        assert (
            self.funds_available[plf.asset_names] - amount >= 0
        ), "insufficient funds to provide liquidity"

        self.funds_available[plf.asset_names] -= amount

        # update liquidity pool
        plf.total_available_funds += amount

        # update i tokens of the user in the pool registry
        plf.user_i_tokens[self.name] += amount

        # matching balance in user's account to pool registry record
        self.funds_available[plf.interest_token_name] = plf.user_i_tokens[self.name]

    def borrow_repay(self, amount: float, plf: Plf):

        if self.name not in plf.user_b_tokens:
            plf.user_b_tokens[self.name] = 0

        if plf.borrow_token_name not in self.funds_available:
            self.funds_available[plf.borrow_token_name] = 0

        if plf.user_b_tokens[self.name] + amount < 0:
            raise ValueError("cannot repay more b-tokens than you have")

        if self.funds_available[plf.interest_token_name] * plf.collateral_factor <= (
            amount + self.funds_available[plf.borrow_token_name]
        ):
            raise ValueError(
                "insufficient collateral to get the amount of requested debt tokens"
            )

        # update liquidity pool
        plf.total_borrowed_funds += amount
        plf.total_available_funds -= amount

        # update b tokens of the user in the pool registry
        plf.user_b_tokens[self.name] += amount

        # matching balance in user's account to pool registry record
        self.funds_available[plf.borrow_token_name] = plf.user_b_tokens[self.name]

        self.funds_available[plf.asset_names] += amount


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


@dataclass
class Plf:
    env: Env
    initiator: User
    reward_token_name: str = "aave"
    # supply_apy: float = 0.06
    # borrow_apy: float = 0.07
    initial_starting_funds: float = 1000
    collateral_factor: float = 0.85
    asset_names: str = "dai"  # you can only deposit and borrow 1 token

    def __post_init__(self):
        self.total_available_funds = self.initial_starting_funds
        self.total_borrowed_funds = 0.0  # start with no funds borrowed

        available_prices = self.env.prices
        self.interest_token_name = INTEREST_TOKEN_PREFIX + self.asset_names
        self.borrow_token_name = DEBT_TOKEN_PREFIX + self.asset_names

        assert (
            self.asset_names in self.initiator.funds_available
            and self.initiator.funds_available[self.asset_names]
            >= self.initial_starting_funds
        ), "insufficient funds"

        # deduct funds from user balance
        self.initiator.funds_available[self.asset_names] -= self.initial_starting_funds

        self.user_i_tokens = {self.initiator.name: self.initial_starting_funds}

        self.user_b_tokens = {self.initiator.name: 0.0}

        # add interest-bearing token into initiator's wallet
        self.initiator.funds_available[
            self.interest_token_name
        ] = self.initial_starting_funds
        self.initiator.funds_available[self.borrow_token_name] = 0

        # if reward token is a new token, then initiate price with 0
        reward_token_name = self.reward_token_name
        if reward_token_name not in available_prices:
            available_prices[self.reward_token_name] = 0

    def __repr__(self):
        return f"(available funds = {self.total_available_funds}, borrowed funds = {self.total_borrowed_funds})"

    @property
    def utilization_ratio(self) -> float:
        return self.total_borrowed_funds / (
            self.total_available_funds + self.total_borrowed_funds
        )

    @property
    def supply_apy(self) -> float:
        _, rs = borrow_lend_rates(self.utilization_ratio)
        return rs

    @property
    def borrow_apy(self) -> float:
        rb, _ = borrow_lend_rates(self.utilization_ratio)
        return rb

    @property
    def total_pool_shares(self) -> tuple[float, float]:
        total_i_tokens = sum(self.user_i_tokens.values())
        total_b_tokens = sum(self.user_b_tokens.values())
        return total_i_tokens, total_b_tokens

    @property
    def daily_supplier_multiplier(self) -> float:
        return (1 + self.supply_apy) ** (1 / 365)

    @property
    def daily_borrow_multiplier(self) -> float:
        return (1 + self.borrow_apy) ** (1 / 365)

    def get_user_pool_fraction(self, user_name: str) -> tuple[float, float]:
        if user_name not in self.user_i_tokens:
            self.user_i_tokens[user_name] = self.env.users[user_name].funds_available[
                self.interest_token_name
            ] = 0.0
        i_token_fraction = self.user_i_tokens[user_name] / self.total_pool_shares[0]

        if user_name not in self.user_b_tokens:
            self.user_b_tokens[user_name] = self.env.users[user_name].funds_available[
                self.borrow_token_name
            ] = 0.0

        assert 0 <= self.user_b_tokens[user_name] <= self.total_pool_shares[1]

        if self.total_pool_shares[1] == 0:
            b_token_fraction = 0
        else:
            b_token_fraction = self.user_b_tokens[user_name] / self.total_pool_shares[1]

        return i_token_fraction, b_token_fraction

    def accrue_interest(self):
        for user_name in self.user_i_tokens:
            user_funds = self.env.users[user_name].funds_available

            # distribute i-token
            user_funds[self.interest_token_name] *= self.daily_supplier_multiplier

            # update i token register
            self.user_i_tokens[user_name] = user_funds[self.interest_token_name]

        for user_name in self.user_b_tokens:
            user_funds = self.env.users[user_name].funds_available

            # distribute b-token
            user_funds[self.borrow_token_name] *= self.daily_borrow_multiplier

            # update b token register
            self.user_b_tokens[user_name] = user_funds[self.borrow_token_name]

    def distribute_reward(self, quantity: float):
        for user_name in self.env.users:
            user_funds = self.env.users[user_name].funds_available

            # initialize if the balance does not exist before airdropping
            if self.reward_token_name not in user_funds:
                user_funds[self.reward_token_name] = 0

            # distribute reward token proportionaly
            user_funds[self.reward_token_name] += (
                np.mean(self.get_user_pool_fraction(user_name=user_name)) * quantity
            )
