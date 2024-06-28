from abc import ABC
from currency_quote.application.ports.inbound.controller import IController
from currency_quote.application.use_cases.get_last_currency_quote import GetLastCurrencyQuoteUseCase
from currency_quote.application.use_cases.get_history_currency_quote import GetHistCurrencyQuoteUseCase
from currency_quote.domain.entities.currency import CurrencyQuote


class ClientBuilder(IController):
    def __init__(self, currency: CurrencyQuote):
        self.currency = currency

    def get_last_quote(self) -> dict:
        return GetLastCurrencyQuoteUseCase.execute(currency_list=self.currency.get_currency_list())

    def get_history_quote(self, reference_date: int) -> dict:
        return GetHistCurrencyQuoteUseCase.execute(
            currency_list=self.currency.get_currency_list(),
            reference_date=reference_date
        )
