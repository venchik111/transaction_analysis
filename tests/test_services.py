import json
from datetime import datetime

import pandas as pd
import pytest

from src.services import simple_search


@pytest.mark.parametrize(
    "search, expected",
    [
        ("ЛЕН", [1]),
        ("сУпЕр", [1, 2]),
        ("мтс", [3]),
        ("нет совпадений", []),
        ("", [1, 2, 3, 4]),
        (".*", []),
    ],
)
def test_simple_search(search: str, expected: list[int]) -> None:
    operations = [
        {"id": 1, "Описание": "Лента", "Категория": "Супермаркеты"},
        {"id": 2, "Описание": "Магнит", "Категория": "Супермаркеты"},
        {"id": 3, "Описание": "МТС", "Категория": None},
        {"id": 4},
    ]
    result = json.loads(simple_search(operations, search))
    assert [item["id"] for item in result] == expected


def test_simple_search_dates_and_missing() -> None:
    operations = [
        {"Описание": "Лента", "Дата операции": datetime(2021, 12, 1), "MCC": float("nan")},
        {"Описание": "Лента", "Дата операции": pd.NaT, "MCC": None},
    ]
    result = json.loads(simple_search(operations, "лента"))
    assert result[0]["Дата операции"] == "2021-12-01 00:00:00"
    assert result[0]["MCC"] is None
    assert result[1]["Дата операции"] is None


def test_simple_search_empty() -> None:
    assert simple_search([], "Лента") == "[]"
