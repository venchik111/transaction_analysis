import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number, expected_result",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("700079228960636123456", "it's not card number"),
        (7000792289606361, "7000 79** **** 6361"),
        ("xaxaxa burmalda", "it's not card number"),
    ],
)
def test_get_mask_card_number(number, expected_result):
    assert get_mask_card_number(number) == expected_result


@pytest.mark.parametrize(
    "account, expected_result",
    [
        ("73654108430135874305", "**4305"),
        ("73654108430135874305678123456890", "**6890"),
        (73654108430135874305, "**4305"),
        ("7365410843013", "**3013"),
    ],
)
def test_get_mask_account(account, expected_result):
    assert get_mask_account(account) == expected_result
