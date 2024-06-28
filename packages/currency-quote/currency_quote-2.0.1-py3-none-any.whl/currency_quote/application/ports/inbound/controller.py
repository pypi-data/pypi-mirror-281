from abc import ABC, abstractmethod, abstractclassmethod
from currency_quote.domain.entities.currency import CurrencyQuote


class IController(ABC):

    @abstractmethod
    def __init__(self, currency: CurrencyQuote):
        self.currency = currency

    @abstractmethod
    def get_last_quote(self) -> dict:
        pass

    @abstractmethod
    def get_history_quote(self, reference_date: int) -> dict:
        pass
