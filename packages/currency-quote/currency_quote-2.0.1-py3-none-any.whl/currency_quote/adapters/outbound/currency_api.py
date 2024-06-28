from api_to_dataframe import ClientBuilder, RetryStrategies
from currency_quote.application.ports.outbound.currency_repository import ICurrencyRepository
from currency_quote.config.endpoints import API


class CurrencyAPI(ICurrencyRepository):
    def __init__(self, currency_codes: str):
        self.currency_codes = currency_codes

    def get_last_quote(self) -> dict:
        url = f"{API.ENDPOINT_LAST_COTATION}{self.currency_codes}"
        client = ClientBuilder(
            endpoint=url,
            retry_strategy=RetryStrategies.ExponentialRetryStrategy
        )

        response = client.get_api_data()

        return response

    def get_history_quote(self, reference_date: int) -> dict:
        pass
    