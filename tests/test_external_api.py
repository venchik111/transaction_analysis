from typing import Any
from unittest.mock import Mock, patch

from src.external_api import get_transaction_amount


@patch("src.external_api.requests.get")
def test_get_transaction_amount_rub(
    mock_get: Mock,
    rub_transaction: dict[str, Any],
) -> None:
    result = get_transaction_amount(rub_transaction)

    assert result == 1000.0
    mock_get.assert_not_called()


@patch("src.external_api.requests.get")
def test_get_transaction_amount_usd(
    mock_get: Mock,
    usd_transaction: dict[str, Any],
) -> None:
    mock_response = Mock()

    mock_response.json.return_value = {
        "result": 9000.0,
    }

    mock_get.return_value = mock_response

    result = get_transaction_amount(usd_transaction)

    assert result == 9000.0
    mock_get.assert_called_once()
