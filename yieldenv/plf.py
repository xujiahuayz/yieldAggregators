from dataclasses import dataclass
import logging
import numpy as np
from numpy.core.arrayprint import ComplexFloatingFormat


class Plf:
    def __init__(
        self,
        supply_rate: float,
        borrow_rate: float,
        distribution_per_day: float,
        total_available_funds: float = 100,
        collateral_ratio: float = 1.2,
    ):
        self.supply_apr = supply_rate
        self.borrow_apr = borrow_rate
        self.total_available_funds = total_available_funds
        self.collateral_ratio = (
            collateral_ratio
            # collateral divided by amount able to borrow
        )
        self.distribution_per_day = distribution_per_day
        self.user_interest_revenue = 0
        self.paid_fees = 0
        self.user_collected_tokens = 0
        self.user_deposit_available_as_collateral = (
            0  # imagine there is only one user interacting with the pool
        )
        # self.user_borrow = 0

    def supply(self, amount, days):

        self.total_available_funds += amount
        self.user_interest_revenue += amount * (self.supply_apr / 365) * days

        self.user_deposit_available_as_collateral += amount

        self.user_collected_tokens += (
            amount / self.total_available_funds * self.distribution_per_day * days
        )  # this assumes that the portion of supplied tokens is constant throughout the supplying period

    def borrow(self, amount: float, days: float):
        collateral = amount * self.collateral_ratio
        assert (
            self.user_deposit_available_as_collateral >= collateral
        ), "Borrow position under-collateralized"

        self.user_deposit_available_as_collateral -= amount
        self.total_available_funds -= amount

        self.paid_fees += amount * (self.borrow_apr / 365) * days

        self.user_collected_tokens += (
            amount / self.total_available_funds * self.distribution_per_day * days
        )  # this assumes that the portion of supplied tokens is constant throughout the supplying period

    def supply_then_borrow(self, amount, days):
        collateral = amount * self.collateral_ratio
        self.supply(amount=collateral, days=days)
        self.borrow(amount=amount, days=days)

    def getProfit(self, token_price):

        fees = self.user_interest_revenue - self.paid_fees
        tokens = self.user_collected_tokens
        value = tokens * token_price

        return (
            "Collected fees (in supplied token): "
            + str(fees)
            + ". Collected tokens: "
            + str(tokens)
            + ", worth: "
            + str(value)
        )
