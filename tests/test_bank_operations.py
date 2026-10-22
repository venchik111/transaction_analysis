import pytest

from src.bank_operations import process_bank_operations, process_bank_search


@pytest.mark.parametrize(
    "search, expected_ids",
    [
        ("организации", [1, 3]),
        ("Перевод", [1, 2, 3, 5]),
        ("перевод", [1, 2, 3, 5]),
        ("вклада", [4]),
        ("несуществующее", []),
    ],
)
def test_process_bank_search(
    bank_operations: list[dict],
    search: str,
    expected_ids: list[int],
) -> None:
    result = process_bank_search(bank_operations, search)

    assert [operation["id"] for operation in result] == expected_ids


def test_process_bank_search_empty_list() -> None:
    result = process_bank_search([], "Перевод")

    assert result == []


def test_process_bank_operations(
    bank_operations: list[dict],
) -> None:
    categories = [
        "Перевод организации",
        "Открытие вклада",
        "Перевод с карты на карту",
    ]

    result = process_bank_operations(
        bank_operations,
        categories,
    )

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Перевод с карты на карту": 1,
    }


def test_process_bank_operations_unknown_category(
    bank_operations: list[dict],
) -> None:
    categories = [
        "Перевод организации",
        "Несуществующая операция",
    ]

    result = process_bank_operations(
        bank_operations,
        categories,
    )

    assert result == {
        "Перевод организации": 2,
        "Несуществующая операция": 0,
    }


def test_process_bank_operations_empty_list() -> None:
    result = process_bank_operations(
        [],
        ["Перевод организации"],
    )

    assert result == {
        "Перевод организации": 0,
    }
