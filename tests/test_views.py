import json
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import get_cards, get_greeting, get_top_transactions, main_page


@pytest.mark.parametrize(
    "hour, minute, expected",
    [
        (0, 0, "Доброй ночи"),
        (5, 59, "Доброй ночи"),
        (6, 0, "Доброе утро"),
        (11, 59, "Доброе утро"),
        (12, 0, "Добрый день"),
        (17, 59, "Добрый день"),
        (18, 0, "Добрый вечер"),
        (22, 59, "Добрый вечер"),
        (23, 0, "Доброй ночи"),
    ],
)
def test_get_greeting(hour: int, minute: int, expected: str) -> None:
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 10, 22, hour, minute)
        assert get_greeting() == expected


def test_get_cards(course_transactions: pd.DataFrame) -> None:
    operations = course_transactions.loc[course_transactions["Статус"] == "OK"]
    result = get_cards(operations)
    assert result == [
        {"last_digits": "1112", "total_spent": 1005.5, "cashback": 10.05},
        {"last_digits": "5091", "total_spent": 50.0, "cashback": 0.5},
    ]


def test_get_top_transactions(course_transactions: pd.DataFrame) -> None:
    result = get_top_transactions(course_transactions)
    assert len(result) == 5
    assert [item["amount"] for item in result] == [1000, -20, -50, -75, -80]
    assert result[0] == {"date": "12.12.2021", "amount": 1000, "category": "Пополнения", "description": "Зарплата"}
    assert result[1]["category"] is None


def test_main_page(course_transactions: pd.DataFrame) -> None:
    settings = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    with (
        patch("src.views.load_operations", return_value=course_transactions),
        patch("src.views.load_settings", return_value=settings),
        patch("src.views.get_greeting", return_value="Добрый день"),
        patch("src.views.get_currency_rates", return_value=[{"currency": "USD", "rate": 90.0}]) as currencies,
        patch("src.views.get_stock_prices", return_value=[{"stock": "AAPL", "price": 150.0}]) as stocks,
    ):
        result = json.loads(main_page("2021-12-20 12:00:00"))

    assert result["greeting"] == "Добрый день"
    assert result["cards"] == [
        {"last_digits": "1112", "total_spent": 425.5, "cashback": 4.25},
        {"last_digits": "5091", "total_spent": 50.0, "cashback": 0.5},
    ]
    assert [item["amount"] for item in result["top_transactions"]] == [1000, -20, -50, -75, -100]
    assert result["currency_rates"] == [{"currency": "USD", "rate": 90.0}]
    assert result["stock_prices"] == [{"stock": "AAPL", "price": 150.0}]
    currencies.assert_called_once_with(["USD"])
    stocks.assert_called_once_with(["AAPL"])


def test_main_page_empty(course_transactions: pd.DataFrame) -> None:
    with (
        patch("src.views.load_operations", return_value=course_transactions),
        patch("src.views.load_settings", return_value={"user_currencies": [], "user_stocks": []}),
    ):
        result = json.loads(main_page("2020-01-01 00:00:00"))
    assert result["cards"] == []
    assert result["top_transactions"] == []


def test_top_less_than_five(course_transactions: pd.DataFrame) -> None:
    assert len(get_top_transactions(course_transactions.head(2))) == 2
