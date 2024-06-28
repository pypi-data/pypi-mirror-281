import pytest
from currency_quote.application.use_cases.get_last_currency_quote import GetLastCurrencyQuoteUseCase


def test_valid_currency():
    currency_list = ["USD-BRL", "EUR-BRL"]
    result = GetLastCurrencyQuoteUseCase.execute(currency_list=currency_list)
    assert isinstance(result, dict)
    assert len(result) == 2


def test_partial_valid_currency():
    currency_list = ["USD-BRL", "EUR-BRL", "param1"]
    expected_result = ["USD-BRL", "EUR-BRL"]
    result = GetLastCurrencyQuoteUseCase.execute(currency_list=currency_list)
    assert isinstance(result, dict)
    assert len(result) == 2


def test_invalid_currency():
    currency_list = ["param1", "param2"]
    with pytest.raises(ValueError):
        GetLastCurrencyQuoteUseCase.execute(currency_list=currency_list)
