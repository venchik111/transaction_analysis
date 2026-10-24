from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import save_report, spending_by_category


@pytest.mark.parametrize(
    "end_date, start_date",
    [("2021-02-28", "2020-11-28"), ("2024-05-31", "2024-02-29"), ("2021-12-20", "2021-09-20")],
)
def test_spending_by_category(tmp_path: Path, end_date: str, start_date: str) -> None:
    data = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    f"{start_date} 00:00:00",
                    f"{end_date} 23:59:59",
                    f"{end_date} 12:00:00",
                    f"{end_date} 12:00:00",
                    f"{end_date} 12:00:00",
                ]
            ),
            "Категория": ["Связь", "Связь", "Связь", "Связь", "Такси"],
            "Статус": ["OK", "OK", "FAILED", "OK", "OK"],
            "Сумма платежа": [-10, -20, -30, 40, -50],
        }
    )
    outside = data.iloc[[0, 1]].copy()
    outside.iloc[0, 0] -= pd.Timedelta(seconds=1)
    outside.iloc[1, 0] += pd.Timedelta(seconds=1)
    operations = pd.concat([data, outside], ignore_index=True)
    original = operations.copy(deep=True)

    with patch("src.decorators.BASE_DIR", tmp_path):
        result = spending_by_category(operations, "Связь", end_date)

    pd.testing.assert_frame_equal(result, data.iloc[:2])
    pd.testing.assert_frame_equal(operations, original)
    saved = pd.read_excel(tmp_path / "reports" / "spending_by_category.xlsx")
    pd.testing.assert_frame_equal(saved, result, check_dtype=False)


def test_report_current_date(tmp_path: Path, course_transactions: pd.DataFrame) -> None:
    with patch("src.decorators.BASE_DIR", tmp_path), patch("src.reports.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2021, 12, 20, 12)
        result = spending_by_category(course_transactions, "Связь")
    assert result["Описание"].tolist() == ["МТС"]


def test_report_empty(tmp_path: Path, course_transactions: pd.DataFrame) -> None:
    with patch("src.decorators.BASE_DIR", tmp_path):
        result = spending_by_category(course_transactions, "Нет категории", "2021-12-20")
    assert result.empty
    assert result.columns.tolist() == course_transactions.columns.tolist()
    assert pd.read_excel(tmp_path / "reports" / "spending_by_category.xlsx").empty


def test_save_report_filename(tmp_path: Path, course_transactions: pd.DataFrame) -> None:
    file_path = tmp_path / "nested" / "report.xlsx"

    @save_report(file_path)
    def make_report(data: pd.DataFrame, count: int) -> pd.DataFrame:
        return data.head(count)

    result = make_report(course_transactions, count=2)
    saved = pd.read_excel(file_path)
    assert make_report.__name__ == "make_report"
    pd.testing.assert_frame_equal(saved, result, check_dtype=False)
