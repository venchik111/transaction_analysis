import json
import logging
from datetime import datetime

import pandas as pd

from src.external_api import get_currency_rates, get_stock_prices
from src.utils import (
    BASE_DIR,
    load_operations,
    load_settings,
    transactions_to_json,
)
from src.widget import get_date

logger = logging.getLogger(__name__)


def get_greeting() -> str:
    """Возвращает приветствие по текущему времени."""
    hour = datetime.now().hour

    if 6 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_cards(transactions: pd.DataFrame) -> list[dict]:
    """Считает расходы и кешбэк по каждой карте."""
    result = []

    for card, operations in transactions.groupby("Номер карты"):
        expenses = operations.loc[operations["Сумма платежа"] < 0, "Сумма платежа"]
        total_spent = round(float(-expenses.sum()), 2)
        result.append(
            {
                "last_digits": str(card).replace("*", "")[-4:],
                "total_spent": total_spent,
                "cashback": round(total_spent / 100, 2),
            }
        )

    return result


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """Возвращает пять операций по убыванию суммы платежа."""
    top = transactions.sort_values("Сумма платежа", ascending=False).head(5)
    top = top[["Дата операции", "Сумма платежа", "Категория", "Описание"]].copy()
    top["Дата операции"] = top["Дата операции"].dt.strftime("%Y-%m-%dT%H:%M:%S").apply(get_date)
    top.columns = ["date", "amount", "category", "description"]
    return json.loads(transactions_to_json(top))


def main_page(date: str) -> str:
    """Формирует JSON для главной страницы за указанный период."""
    end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)
    transactions = load_operations(BASE_DIR / "data" / "operations.xlsx")
    transactions = transactions.loc[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Статус"] == "OK")
    ]
    settings = load_settings()

    result = {
        "greeting": get_greeting(),
        "cards": get_cards(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }

    logger.info("Сформирована главная страница на %s", date)
    return json.dumps(result, ensure_ascii=False, allow_nan=False)
