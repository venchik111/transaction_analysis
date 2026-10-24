import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.utils import load_transactions, load_transactions_csv, load_transactions_excel


def test_load_transactions(tmp_path: Path) -> None:
    """Проверяет корректное чтение JSON-файла."""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]

    file_path = tmp_path / "operations.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(transactions, file)

    result = load_transactions(str(file_path))

    assert result == transactions


def test_load_transactions_empty_file(tmp_path: Path) -> None:
    """Проверяет чтение пустого JSON-файла."""
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")

    result = load_transactions(str(file_path))

    assert result == []


def test_load_transactions_not_list(tmp_path: Path) -> None:
    """Проверяет JSON-файл, содержащий не список."""
    file_path = tmp_path / "operations.json"

    data = {
        "id": 1,
        "state": "EXECUTED",
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)

    result = load_transactions(str(file_path))

    assert result == []


def test_load_transactions_file_not_found() -> None:
    """Проверяет обработку отсутствующего JSON-файла."""
    result = load_transactions("file_that_does_not_exist.json")

    assert result == []


def test_load_transactions_csv(
    tmp_path: Path,
    table_transactions: list[dict[str, Any]],
) -> None:
    """Проверяет чтение финансовых операций из CSV."""
    file_path = tmp_path / "transactions.csv"

    data_frame = pd.DataFrame(table_transactions)
    data_frame.to_csv(
        file_path,
        sep=";",
        index=False,
    )

    result = load_transactions_csv(str(file_path))

    assert result == table_transactions


def test_load_transactions_excel(
    tmp_path: Path,
    table_transactions: list[dict[str, Any]],
) -> None:
    """Проверяет чтение финансовых операций из XLSX."""
    file_path = tmp_path / "transactions.xlsx"

    data_frame = pd.DataFrame(table_transactions)
    data_frame.to_excel(
        file_path,
        index=False,
    )

    result = load_transactions_excel(str(file_path))

    assert result == table_transactions
