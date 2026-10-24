from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import get_api_data, get_currency_rates, get_stock_prices


@pytest.fixture(autouse=True)
def skip_api_delay(monkeypatch) -> None:
    monkeypatch.setattr("src.external_api.sleep", lambda seconds: None)


def test_get_api_data(monkeypatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")
    response = Mock()
    response.json.return_value = {"value": 123}
    with (
        patch("src.external_api.requests.get", return_value=response) as mock_get,
        patch("src.external_api.sleep") as delay,
    ):
        assert get_api_data({"function": "GLOBAL_QUOTE"}) == {"value": 123}
        delay.assert_called_once_with(1)
    assert mock_get.call_args.kwargs["timeout"] == 10
    assert mock_get.call_args.kwargs["params"]["apikey"] == "test-key"
    response.raise_for_status.assert_called_once()


@pytest.mark.parametrize("error", [requests.Timeout, requests.ConnectionError, requests.HTTPError, ValueError])
def test_api_errors(monkeypatch, error, caplog) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "secret-test-key")
    with patch("src.external_api.requests.get", side_effect=error("secret-test-key")):
        assert get_api_data({}) == {}
    assert "secret-test-key" not in caplog.text


@pytest.mark.parametrize(
    "response_data", [{"Note": "limit"}, {"Information": "limit"}, {"Error Message": "error"}, []]
)
def test_api_invalid_response(monkeypatch, response_data) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")
    response = Mock()
    response.json.return_value = response_data
    with patch("src.external_api.requests.get", return_value=response):
        assert get_api_data({}) == {}


def test_api_bad_json(monkeypatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")
    response = Mock()
    response.json.side_effect = ValueError("invalid JSON")
    with patch("src.external_api.requests.get", return_value=response):
        assert get_api_data({}) == {}


def test_api_missing_key(monkeypatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "")
    with patch("src.external_api.requests.get") as mock_get:
        assert get_api_data({}) == {}
    mock_get.assert_not_called()


def test_currency_rates() -> None:
    responses = [{"Realtime Currency Exchange Rate": {"5. Exchange Rate": "90.5"}}, {}]
    with patch("src.external_api.get_api_data", side_effect=responses) as api:
        result = get_currency_rates(["USD", "EUR"])
    assert result == [{"currency": "USD", "rate": 90.5}, {"currency": "EUR", "rate": None}]
    assert api.call_args_list[0].args[0]["to_currency"] == "RUB"


def test_stock_prices() -> None:
    with patch("src.external_api.get_api_data", side_effect=[{"Global Quote": {"05. price": "150"}}, {}]):
        result = get_stock_prices(["AAPL", "MSFT"])
    assert result == [{"stock": "AAPL", "price": 150.0}, {"stock": "MSFT", "price": None}]


@pytest.mark.parametrize("value", ["0", "-1", "nan", "inf", "wrong", None])
def test_quotes_invalid_values(value) -> None:
    with patch(
        "src.external_api.get_api_data", return_value={"Realtime Currency Exchange Rate": {"5. Exchange Rate": value}}
    ):
        assert get_currency_rates(["USD"])[0]["rate"] is None
    with patch("src.external_api.get_api_data", return_value={"Global Quote": {"05. price": value}}):
        assert get_stock_prices(["AAPL"])[0]["price"] is None
