from currency_quote import CurrencyQuote, ClientBuilder
import pytest


@pytest.fixture()
def client():
    return ClientBuilder(currency=CurrencyQuote(currency_list=["USD-BRL"]))


def test_client_builder(client):
    assert isinstance(client, ClientBuilder)


def test_get_last_quote(client):
    last_quote = client.get_last_quote()
    assert isinstance(last_quote, dict)


def test_get_hist_quote(client):
    hist_quote = client.get_history_quote(reference_date=20230101)
    assert isinstance(hist_quote, dict)
