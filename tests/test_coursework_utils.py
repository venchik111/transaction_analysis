import json
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.utils import BASE_DIR, load_operations, load_settings, setup_logging


def test_load_operations(tmp_path: Path) -> None:
    file_path = tmp_path / "operations.xlsx"
    pd.DataFrame(
        {
            "Дата операции": ["01.12.2021 12:00:00", "ошибка"],
            "Дата платежа": ["02.12.2021", None],
            "Номер карты": ["0012", None],
        }
    ).to_excel(file_path, index=False)
    result = load_operations(file_path)
    assert result.loc[0, "Дата операции"] == pd.Timestamp("2021-12-01 12:00:00")
    assert result.loc[0, "Дата платежа"] == pd.Timestamp("2021-12-02")
    assert result.loc[0, "Номер карты"] == "0012"
    assert pd.isna(result.loc[1, "Дата операции"])


def test_load_real_excel() -> None:
    result = load_operations(BASE_DIR / "data" / "operations.xlsx")
    assert not result.empty
    assert pd.api.types.is_datetime64_any_dtype(result["Дата операции"])
    assert {"Статус", "Сумма платежа", "Категория", "Описание", "Номер карты"} <= set(result.columns)
    assert (result["Сумма платежа"] < 0).any()


def test_settings(tmp_path: Path) -> None:
    settings = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    (tmp_path / "user_settings.json").write_text(json.dumps(settings), encoding="utf-8")
    with patch("src.utils.BASE_DIR", tmp_path):
        assert load_settings() == settings


def test_setup_logging(tmp_path: Path) -> None:
    with patch("src.utils.BASE_DIR", tmp_path), patch("src.utils.logging.basicConfig") as config:
        setup_logging()
    assert (tmp_path / "logs").is_dir()
    assert config.call_args.kwargs["filename"] == tmp_path / "logs" / "app.log"
