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
    

    def supply(self, amount):
        self.total_available_funds += amount
    
    def stopSupply(self, amount):
        self.total_available_funds -= amount

    def borrow(self, amount: float):
        self.total_borrowed_funds += amount

    def stopBorrow(self, amount: float): # = paying back loan
        self.total_borrowed_funds -= amount


class User:
    def __init__(self, name: str):
        self.user_collected_tokens = 0
        self.user_deposit_available_as_collateral = 0 #keep track of user funds available
        self.user_borrowed_funds = 0 #keep track of user borrowed funds
        self.user_interest_revenue = 0
        self.user_paid_interest = 0
        self.name = name

    def startSupplying(self, amount: float, plf: Plf):
        plf.supply(amount)
        self.user_deposit_available_as_collateral += amount

    def stopSupplying(self, amount: float, plf: Plf):
        plf.stopSupply(amount)
        self.user_deposit_available_as_collateral -= amount

    def startBorrowing(self, amount: float, plf: Plf):
        collateral = amount * plf.collateral_ratio
        assert (
            self.user_deposit_available_as_collateral >= collateral
        ), "Borrow position under-collateralized"
        plf.borrow(amount, collateral)
        self.user_deposit_available_as_collateral -= collateral
        self.user_borrowed_funds +=amount

    def stopBorrowing(self, amount: float, plf: Plf): # = paying back loan
        collateral = amount * plf.collateral_ratio

        plf.stopBorrow(amount)
        self.user_deposit_available_as_collateral += collateral
        self.user_borrowed_funds -=amount


    def getProfit(self, token_price: float, plf: Plf):

        interest_revenue = self.user_deposit_available_as_collateral * (plf.supply_apr/365)
        interest_cost = self.user_borrowed_funds * (plf.borrow_apr/365)

        yield_interest = interest_revenue - interest_cost

        tokens_for_supplying = (self.user_deposit_available_as_collateral/plf.total_available_funds) * plf.distribution_per_day * 0.5 # 50% goes to suppliers
        tokens_for_borrowing = (self.user_borrowed_funds/plf.total_borrowed_funds) * plf.distribution_per_day * 0.5 # 50% goes to borrowers 
        yield_tokens = tokens_for_supplying + tokens_for_borrowing

        value_yield_tokens = yield_tokens * token_price

        total_yield = yield_interest + value_yield_tokens

        return (yield_interest, yield_tokens, value_yield_tokens, total_yield)


