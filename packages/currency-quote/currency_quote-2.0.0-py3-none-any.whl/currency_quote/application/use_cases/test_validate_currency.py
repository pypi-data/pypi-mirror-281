import pytest
from currency_quote.application.use_cases.validate_currency import ValidateCurrencyUseCase


def test_valid_currency():
    currency_list = ["USD-BRL", "USD-BRLT"]
    result = ValidateCurrencyUseCase.execute(currency_list=currency_list)
    assert result == currency_list


def test_partial_valid_currency():
    currency_list = ["USD-BRL", "USD-BRLT", "param1"]
    expected_result = ["USD-BRL", "USD-BRLT"]
    result = ValidateCurrencyUseCase.execute(currency_list=currency_list)
    assert result == expected_result


def test_invalid_currency():
    currency_list = ["param1", "param2"]
    with pytest.raises(ValueError):
        ValidateCurrencyUseCase.execute(currency_list=currency_list)
