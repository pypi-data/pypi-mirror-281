# src/currency_quote/application/ports/outbound/currency_validator_port.py
from abc import ABC, abstractmethod


class ICurrencyValidator(ABC):

    @abstractmethod
    def __init__(self, currency_list: list):
        pass

    @abstractmethod
    def validate_currency_code(self) -> list:
        pass
