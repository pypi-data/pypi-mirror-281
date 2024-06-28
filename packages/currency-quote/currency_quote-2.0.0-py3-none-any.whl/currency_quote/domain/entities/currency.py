# currency.py

class CurrencyQuote:
    def __init__(self, currency_list: list):
        self.currency_list = currency_list

    def get_currency_list(self) -> list:
        if self.currency_list is None:
            raise ValueError("Currency list is empty")

        return self.currency_list
