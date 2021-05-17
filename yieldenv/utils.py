from collections.abc import MutableMapping
import warnings

from yieldenv.constants import INTEREST_TOKEN_PREFIX, DEBT_TOKEN_PREFIX


class PriceDict(MutableMapping):
    # def __getitem__(self, key):
    #     return dict.__getitem__(self, key)
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
