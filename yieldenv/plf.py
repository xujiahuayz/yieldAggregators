from dataclasses import dataclass
import dataclasses
import logging
import numpy as np


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
        self.total_borrowed_funds += amount

    def process_repay(self, amount: float):  # = paying back loan
        self.total_borrowed_funds -= amount


class User:
    def __init__(self, name: str, plf: Plf):
        self.plf = plf
        self.collected_tokens = 0
        self.deposit = 0
        # self.deposit_available_as_collateral = 0  # keep track of user funds available
        self.borrowed_funds = 0  # keep track of user borrowed funds
        # self.interest_revenue = 0
        # self.paid_interest = 0
        self.name = name

    def supply(self, amount: float, plf: Plf):
        plf.process_supply(amount)
        self.deposit += amount

        # self.deposit_available_as_collateral += amount

    def withdraw(self, amount: float, plf: Plf):
        plf.process_withdraw(amount)
        self.deposit -= amount
        # self.deposit_available_as_collateral -= amount

    @property
    def deposit_available_as_collateral(self) -> float:
        return self.deposit - self.borrowed_funds * self.plf.collateral_ratio

    def borrow(self, amount: float):
        minimum_deposit_available_needed = amount * self.plf.collateral_ratio
        assert (
            self.deposit_available_as_collateral >= minimum_deposit_available_needed
        ), "Borrow position under-collateralized"
        self.plf.process_borrow(amount)
        self.borrowed_funds += amount

    def repay(self, amount: float, plf: Plf):  # = paying back loan

        plf.process_repay(amount)
        self.borrowed_funds -= amount

    def calculate_profit(self, token_price: float, plf: Plf):

        daily_interest_revenue = self.deposit * (plf.supply_apr / 365)
        daily_interest_cost = self.borrowed_funds * np.exp(plf.borrow_apr / 365)

        yield_interest = daily_interest_revenue - daily_interest_cost

        # Governance token distribution ---
        tokens_for_supplying = (
            (self.deposit / plf.total_available_funds) * plf.distribution_per_day * 0.5
        )  # 50% goes to suppliers
        tokens_for_borrowing = (
            (self.borrowed_funds / plf.total_borrowed_funds)
            * plf.distribution_per_day
            * 0.5
        )  # 50% goes to borrowers
        yield_tokens = tokens_for_supplying + tokens_for_borrowing

        value_yield_tokens = yield_tokens * token_price

        total_yield = yield_interest + value_yield_tokens

        return (yield_interest, yield_tokens, value_yield_tokens, total_yield)
