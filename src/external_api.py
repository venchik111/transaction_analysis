import logging
import math
import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.utils import BASE_DIR

load_dotenv()

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY", "")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_transaction_amount(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    headers = {"apikey": API_KEY}

    params = {
        "amount": amount,
        "from": currency,
        "to": "RUB",
    }

    response = requests.get(
        API_URL,
        headers=headers,
        params=params,
    )

    response.raise_for_status()

    result = response.json()

    return float(result["result"])


def get_api_data(params: dict[str, str]) -> dict[str, Any]:
    """Получает ответ API без записи ключа в лог."""
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "")

    if not api_key:
        logger.warning("Не задан ALPHA_VANTAGE_API_KEY")
        return {}

    try:
        response = requests.get(ALPHA_VANTAGE_URL, params={**params, "apikey": api_key}, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            logger.error("API вернул ответ неверного формата")
            return {}

        if any(key in data for key in ["Error Message", "Note", "Information"]):
            logger.warning("API вернул ошибку или ограничение запросов")
            return {}

        return data

    except requests.RequestException, ValueError:
        logger.error("Не удалось получить ответ API")
        return {}


def get_currency_rates(currencies: list[str]) -> list[dict]:
    """Возвращает курсы указанных валют к рублю."""
    result = []

    for currency in currencies:
        data = get_api_data(
            {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": currency,
                "to_currency": "RUB",
            }
        )
        rate = None

        try:
            value = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            if math.isfinite(value) and value > 0:
                rate = value
        except KeyError, TypeError, ValueError:
            pass

        if rate is None:
            logger.warning("Нет курса валюты %s", currency)

        result.append({"currency": currency, "rate": rate})

    return result


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """Возвращает последние доступные цены акций в долларах."""
    result = []

    for stock in stocks:
        data = get_api_data({"function": "GLOBAL_QUOTE", "symbol": stock})
        price = None

        try:
            value = float(data["Global Quote"]["05. price"])
            if math.isfinite(value) and value > 0:
                price = value
        except KeyError, TypeError, ValueError:
            pass

        if price is None:
            logger.warning("Нет цены акции %s", stock)

        result.append({"stock": stock, "price": price})

    return result
