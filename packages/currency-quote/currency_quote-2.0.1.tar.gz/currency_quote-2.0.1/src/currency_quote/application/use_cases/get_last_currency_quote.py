# src/currency_quote/application/use_cases/validate_currency.py
from currency_quote.adapters.outbound.currency_api import CurrencyAPI
from currency_quote.domain.services.get_currency_quote import GetCurrencyQuoteService
from currency_quote.domain.entities.currency import CurrencyQuote


class GetLastCurrencyQuoteUseCase:
    @staticmethod
    def execute(currency_list: list) -> dict:
        currency_object = CurrencyQuote(currency_list)
        quote_service = GetCurrencyQuoteService(
            currency=currency_object,
            currency_repository=CurrencyAPI
        )
        return quote_service.last()
