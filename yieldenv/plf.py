from dataclasses import dataclass
import logging
import numpy as np


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
            collateral_ratio  # collateral divided by amount able to borrow
        )
        self.distribution_per_day = distribution_per_day
        self.collected_fees = 0
        self.paid_fees = 0
        self.collected_tokens = 0

    def supply(self, amount, days):

        self.total_available_funds -= amount
        self.collected_fees += amount * (self.supply_apr / 365) * days

        self.collected_tokens += (
            amount / self.total_available_funds * self.distribution_per_day * days
        )  # this assumes that the portion of supplied tokens is constant throughout the supplying period

    def borrow(self, amount, days):

        collateral = amount * self.collateral_ratio

        assert (
            self.total_available_funds + collateral - amount >= 0
        ), "Not enough funds to borrow"  # can only happen in case collateral_ratio < 1

        self.total_available_funds += (
            collateral  # to borrow x, you first have to deposit x * collateral_ratio
        )
        self.total_available_funds -= amount
        self.paid_fees += amount * (self.borrow_apr / 365) * days
        self.collected_fees += collateral * (self.supply_apr / 365) * days

        self.collected_tokens += (
            collateral / self.total_available_funds * self.distribution_per_day * days
        )  # this assumes that the portion of supplied tokens is constant throughout the supplying period

    def getProfit(self, token_price):

        fees = self.collected_fees - self.paid_fees
        tokens = self.collected_tokens
        value = tokens * token_price

        return (
            "Collected fees (in supplied token): "
            + str(fees)
            + ". Collected tokens: "
            + str(tokens)
            + ", worth: "
            + str(value)
        )
