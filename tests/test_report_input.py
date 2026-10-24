from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.reports import spending_by_category


def test_report_accepts_string_dates(tmp_path: Path) -> None:
    transactions = pd.DataFrame(
        {
            "Дата операции": ["02.01.2021 12:00:00", "2021-01-02 18:00:00", "31.12.2020 23:59:59", "не дата"],
            "Категория": ["Связь"] * 4,
            "Статус": ["OK"] * 4,
            "Сумма платежа": [-100, -200, -300, -400],
        }
    )
    original = transactions.copy(deep=True)

    with patch("src.decorators.BASE_DIR", tmp_path):
        result = spending_by_category(transactions, "Связь", "2021-04-02")

    pd.testing.assert_frame_equal(result, original.iloc[:2])
    pd.testing.assert_frame_equal(transactions, original)
    saved = pd.read_excel(tmp_path / "reports" / "spending_by_category.xlsx")
    assert saved["Сумма платежа"].tolist() == [-100, -200]


def test_report_accepts_empty_dataframe(tmp_path: Path) -> None:
    transactions = pd.DataFrame(columns=["Дата операции", "Категория", "Статус", "Сумма платежа"])

    with patch("src.decorators.BASE_DIR", tmp_path):
        result = spending_by_category(transactions, "Связь", "2021-04-02")

    assert result.empty
    assert result.columns.tolist() == transactions.columns.tolist()
    assert (tmp_path / "reports" / "spending_by_category.xlsx").is_file()
