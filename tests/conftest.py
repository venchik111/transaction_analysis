from typing import Any

import pytest


@pytest.fixture
def operations() -> list[dict[str, str]]:
    return [
        {"state": "EXECUTED", "date": "2023-08-26T10:00:00"},
        {"state": "CANCELED", "date": "2023-07-03T10:00:00"},
        {"state": "EXECUTED", "date": "2023-09-10T10:00:00"},
    ]


@pytest.fixture
def rub_transaction() -> dict[str, Any]:
    return {
        "operationAmount": {
            "amount": "1000.00",
            "currency": {
                "name": "руб.",
                "code": "RUB",
            },
        }
    }


@pytest.fixture
def usd_transaction() -> dict[str, Any]:
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD",
            },
        }
    }


@pytest.fixture
def table_transactions() -> list[dict[str, Any]]:
    """Возвращает тестовые данные для CSV и XLSX."""
    return [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": 3598919,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Счет 72731966109147704472",
            "to": "Счет 26722953654475236715",
            "description": "Перевод с карты на карту",
        },
    ]


@pytest.fixture
def transactions() -> list[dict]:
    return [
        {
            "id": 939719570,
            "operationAmount": {
                "currency": {
                    "code": "USD",
                }
            },
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "operationAmount": {
                "currency": {
                    "code": "USD",
                }
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "operationAmount": {
                "currency": {
                    "code": "RUB",
                }
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "operationAmount": {
                "currency": {
                    "code": "USD",
                }
            },
            "description": "Перевод с карты на карту",
        },
        {
            "id": 594226727,
            "operationAmount": {
                "currency": {
                    "code": "RUB",
                }
            },
            "description": "Перевод организации",
        },
    ]


@pytest.fixture
def bank_operations() -> list[dict]:
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "description": "Перевод со счета на счет",
        },
        {
            "id": 3,
            "state": "CANCELED",
            "description": "Перевод организации",
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "description": "Открытие вклада",
        },
        {
            "id": 5,
            "state": "PENDING",
            "description": "Перевод с карты на карту",
        },
    ]


@pytest.fixture
def course_transactions() -> pd.DataFrame:
    data = [
        ("2021-11-30 23:59:59", "*1112", "OK", -500, "Супермаркеты", "До месяца"),
        ("2021-12-01 00:00:00", "*1112", "OK", -100, "Супермаркеты", "Лента"),
        ("2021-12-10 12:00:00", "*1112", "OK", -250.50, "Супермаркеты", "Магнит"),
        ("2021-12-11 12:00:00", "*5091", "OK", -50, "Связь", "МТС"),
        ("2021-12-12 12:00:00", "*5091", "OK", 1000, "Пополнения", "Зарплата"),
        ("2021-12-13 12:00:00", "*5091", "FAILED", -900, "Супермаркеты", "Отказ"),
        ("2021-12-15 12:00:00", None, "OK", -20, None, "Без карты"),
        ("2021-12-20 12:00:00", "*1112", "OK", -75, "Супермаркеты", "На границе"),
        ("2021-12-20 12:00:01", "*1112", "OK", -80, "Супермаркеты", "После границы"),
    ]
    result = pd.DataFrame(
        data,
        columns=["Дата операции", "Номер карты", "Статус", "Сумма платежа", "Категория", "Описание"],
    )
    result["Дата операции"] = pd.to_datetime(result["Дата операции"])
    return result
