import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_result",
    [
        (
            "EXECUTED",
            [
                {"state": "EXECUTED", "date": "2023-08-26T10:00:00"},
                {"state": "EXECUTED", "date": "2023-09-10T10:00:00"},
            ],
        ),
        (
            "CANCELED",
            [
                {"state": "CANCELED", "date": "2023-07-03T10:00:00"},
            ],
        ),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(operations, state, expected_result):
    assert filter_by_state(operations, state) == expected_result


@pytest.mark.parametrize(
    "reverse, expected_result",
    [
        (
            True,
            [
                {"state": "EXECUTED", "date": "2023-09-10T10:00:00"},
                {"state": "EXECUTED", "date": "2023-08-26T10:00:00"},
                {"state": "CANCELED", "date": "2023-07-03T10:00:00"},
            ],
        ),
        (
            False,
            [
                {"state": "CANCELED", "date": "2023-07-03T10:00:00"},
                {"state": "EXECUTED", "date": "2023-08-26T10:00:00"},
                {"state": "EXECUTED", "date": "2023-09-10T10:00:00"},
            ],
        ),
    ],
)
def test_sort_by_date(operations, reverse, expected_result):
    assert sort_by_date(operations, reverse) == expected_result
