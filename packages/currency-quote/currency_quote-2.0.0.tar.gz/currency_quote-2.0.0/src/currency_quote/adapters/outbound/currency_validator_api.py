# src/currency_quote/adapters/outbound/currency_validator_api.py
from api_to_dataframe import ClientBuilder, RetryStrategies
from currency_quote.config.endpoints import API
from currency_quote.application.ports.outbound.currency_validator_repository import ICurrencyValidator


class CurrencyValidatorAPI(ICurrencyValidator):

    def __init__(self, currency_list: list) -> None:
        self.currency_list = currency_list

    def validate_currency_code(self) -> list:
        client = ClientBuilder(
            endpoint=API.ENDPOINT_AVALIABLE_PARITIES,
            retry_strategy=RetryStrategies.LinearRetryStrategy
        )

        valid_list = client.get_api_data()

        validated_list = []

        for currency_code in self.currency_list:
            if currency_code in valid_list:
                validated_list.append(currency_code)

        return validated_list
