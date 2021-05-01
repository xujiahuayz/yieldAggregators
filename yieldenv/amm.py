from dataclasses import dataclass
import logging
import numpy as np


@dataclass
class CPAmm:
    """
    reserves[0] is the numeraire
    fee represents the fraction of **output asset** that got retained within the pool
    """

    initial_reserves: list[float]
    fee: float = 0.005

    def __post_init__(self):
        self.volumes = [0, 0]
        self.fee_retained_by_reserve = [0, 0]

    @property
    def reserves(self):
        return self.initial_reserves

    @property
    def invariant(self):
        return np.prod(self.reserves)

    @property
    def spot_price(self):
        return self.reserves[0] / self.reserves[1]

    @property
    def pool_value(self):
        return self.reserves[0] * 2

    @property
    def value_held(self):
        return self.initial_reserves[0] + self.initial_reserves[1] * self.spot_price

    def __repr__(self):
        return f"(reserves={self.reserves},invariant={self.invariant})"

    def update_liquidity(self, quantity: float, index: int = 0):
        """
        add (quantity>0) or remove (quantity<0) liquidity
        """

        assert index in [0, 1], "reserve_index out of range"
        assert quantity >= -self.reserves[index], "cannot deplete pool"

        index_other = 1 - index
        # liquidity addition must be proportionate
        quantity_other = quantity * self.reserves[index_other] * self.reserves[index]

        self.reserves[index] += quantity
        self.reserves[index_other] += quantity_other

    def sell_to_pool(self, sell_quantity: float, sell_index: int = 0):
        """
        `quantity` means how much quantity to sell (add) to the pool;
        index means which asset it is
        """

        assert sell_quantity >= 0, "must sell a non-negative quantity"
        assert sell_index in [0, 1], "reserve_index out of range"

        old_invariant = self.invariant

        logging.info(self)

        # add sold quantity to the reserve with `reserve_index`
        self.reserves[sell_index] += sell_quantity
        self.volumes[sell_index] += sell_quantity

        # theoretical new quantity of the other reserve
        _new_reserve = old_invariant / self.reserves[sell_index]
        buy_index = 1 - sell_index
        # theoretical quantity purchased
        buy_quantity = self.reserves[buy_index] - _new_reserve
        self.volumes[buy_index] += buy_quantity

        # fee charge
        swap_fee = buy_quantity * self.fee
        # add fee to revenue
        self.fee_retained_by_reserve[buy_index] += swap_fee

        # actual quantity the trader gets
        buy_quantity -= swap_fee

        # actual new quantity of the buy reserve
        self.reserves[buy_index] -= buy_quantity

        logging.debug(
            f"""
            old invariant: {old_invariant}
            Sell {sell_quantity} in asset#{sell_index}, get {buy_quantity} in asset#{buy_index},
            Earned fee: {swap_fee} in asset#{buy_index}
            new invariant: {self.invariant}
            """
        )

        logging.info(self)
