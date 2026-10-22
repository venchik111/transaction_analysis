import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(transactions, currency, expected_ids):
    result = filter_by_currency(transactions, currency)

    assert [operation["id"] for operation in result] == expected_ids


def test_transaction_descriptions(transactions):
    result = transaction_descriptions(transactions)

    assert list(result) == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


@pytest.mark.parametrize(
    "start, end, expected_result",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9999,
            10001,
            [
                "0000 0000 0000 9999",
                "0000 0000 0001 0000",
                "0000 0000 0001 0001",
            ],
        ),
    ],
)
def test_card_number_generator(start, end, expected_result):
    result = card_number_generator(start, end)

    assert list(result) == expected_result
