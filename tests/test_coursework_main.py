import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.main import main


def test_main_home(capsys) -> None:
    with (
        patch("src.main.setup_logging"),
        patch("builtins.input", side_effect=["1", "2021-12-20 23:59:59"]),
        patch("src.main.main_page", return_value='{"cards": []}') as view,
    ):
        main()
    view.assert_called_once_with("2021-12-20 23:59:59")
    assert '{"cards": []}' in capsys.readouterr().out


def test_main_search(course_transactions: pd.DataFrame, capsys) -> None:
    with (
        patch("src.main.setup_logging"),
        patch("src.main.load_operations", return_value=course_transactions),
        patch("builtins.input", side_effect=["2", "МТС"]),
    ):
        main()
    output = capsys.readouterr().out
    result = json.loads(output.splitlines()[-1])
    assert len(result) == 1
    assert result[0]["Описание"] == "МТС"


@pytest.mark.parametrize("date", ["2021-12-20", ""])
def test_main_report(course_transactions: pd.DataFrame, date: str, capsys) -> None:
    with (
        patch("src.main.setup_logging"),
        patch("src.main.load_operations", return_value=course_transactions),
        patch("builtins.input", side_effect=["3", "Связь", date]),
        patch("src.main.spending_by_category", return_value=course_transactions.head(1)) as report,
    ):
        main()
    assert report.call_args.args[1:] == ("Связь", date or None)
    assert "Найдено операций: 1" in capsys.readouterr().out


def test_main_wrong_choice(capsys) -> None:
    with patch("src.main.setup_logging"), patch("builtins.input", return_value="4"):
        main()
    assert "Некорректный пункт меню." in capsys.readouterr().out
