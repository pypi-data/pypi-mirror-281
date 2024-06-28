from currency_quote.application.ports.outbound.currency_repository import ICurrencyRepository
from currency_quote.application.use_cases.validate_currency import ValidateCurrencyUseCase
from currency_quote.domain.entities.currency import CurrencyQuote

from typing import Type


class GetCurrencyQuoteService:
    def __init__(self, currency: CurrencyQuote, currency_repository: Type[ICurrencyRepository]):
        self.currency_list = currency.get_currency_list()
        self.currency_repository = currency_repository

    def last(self) -> dict:
        return self.currency_repository(self.validate_currency_code()).get_last_quote()

    def history(self, reference_date: int) -> dict:
        return dict()

    def validate_currency_code(self) -> str:
        valid_list = ValidateCurrencyUseCase.execute(self.currency_list)
        return ','.join(valid_list)
