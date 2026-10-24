import json
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.utils import load_operations, load_transactions_excel
from src.views import main_page


def test_empty_excel_keeps_columns(tmp_path: Path, course_transactions: pd.DataFrame) -> None:
    file_path = tmp_path / "empty.xlsx"
    course_transactions.head(0).to_excel(file_path, index=False)

    result = load_operations(file_path)

    assert result.empty
    assert result.columns.tolist() == course_transactions.columns.tolist()
    assert pd.api.types.is_datetime64_any_dtype(result["Дата операции"])
    assert load_transactions_excel(str(file_path)) == []


def test_main_page_empty_excel(tmp_path: Path, course_transactions: pd.DataFrame) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    course_transactions.head(0).to_excel(data_dir / "operations.xlsx", index=False)

    with (
        patch("src.views.BASE_DIR", tmp_path),
        patch("src.views.load_settings", return_value={"user_currencies": [], "user_stocks": []}),
    ):
        result = json.loads(main_page("2021-12-20 12:00:00"))

    assert result["cards"] == []
    assert result["top_transactions"] == []


def test_load_mixed_date_formats(tmp_path: Path) -> None:
    file_path = tmp_path / "mixed.xlsx"
    pd.DataFrame(
        {
            "Дата операции": ["02.01.2021 12:00:00", "2021-01-02 12:00:00", "не дата"],
            "Номер карты": ["0012", "0012", "0012"],
        }
    ).to_excel(file_path, index=False)

    result = load_operations(file_path)

    assert result.loc[0, "Дата операции"] == pd.Timestamp("2021-01-02 12:00:00")
    assert result.loc[1, "Дата операции"] == pd.Timestamp("2021-01-02 12:00:00")
    assert pd.isna(result.loc[2, "Дата операции"])
    assert result["Номер карты"].tolist() == ["0012", "0012", "0012"]
