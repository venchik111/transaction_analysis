import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "number, expected_result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("xaxaxa burmalda", "it's not card number"),
    ],
)
def test_mask_account_card(number, expected_result):
    assert mask_account_card(number) == expected_result


@pytest.mark.parametrize(
    "date, expected_result",
    [("2024-03-11T02:26:18.671407", "11.03.2024"), ("burmalda", "wrong data format")],
)
def test_get_date(date, expected_result):
    assert get_date(date) == expected_result
