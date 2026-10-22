from unittest.mock import Mock, patch

from main import main


@patch("main.load_transactions")
def test_main_json(
    mock_load_transactions: Mock,
    capsys,
) -> None:
    """Проверяет выбор JSON-файла."""
    mock_load_transactions.return_value = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "description": "Перевод организации",
            "operationAmount": {
                "currency": {
                    "code": "RUB",
                }
            },
        }
    ]

    user_answers = [
        "1",
        "EXECUTED",
        "нет",
        "нет",
        "нет",
    ]

    with patch(
        "builtins.input",
        side_effect=user_answers,
    ):
        main()

    captured = capsys.readouterr()

    assert "Для обработки выбран JSON-файл." in captured.out
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured.out
    assert "Всего банковских операций в выборке: 1" in captured.out


@patch("main.load_transactions_csv")
def test_main_csv(
    mock_load_transactions_csv: Mock,
    capsys,
) -> None:
    """Проверяет выбор CSV-файла."""
    mock_load_transactions_csv.return_value = []

    user_answers = [
        "2",
        "EXECUTED",
        "нет",
        "нет",
        "нет",
    ]

    with patch(
        "builtins.input",
        side_effect=user_answers,
    ):
        main()

    captured = capsys.readouterr()

    assert "Для обработки выбран CSV-файл." in captured.out


@patch("main.load_transactions_excel")
def test_main_excel(
    mock_load_transactions_excel: Mock,
    capsys,
) -> None:
    """Проверяет выбор XLSX-файла."""
    mock_load_transactions_excel.return_value = []

    user_answers = [
        "3",
        "EXECUTED",
        "нет",
        "нет",
        "нет",
    ]

    with patch(
        "builtins.input",
        side_effect=user_answers,
    ):
        main()

    captured = capsys.readouterr()

    assert "Для обработки выбран XLSX-файл." in captured.out


@patch("main.load_transactions")
def test_main_wrong_status(
    mock_load_transactions: Mock,
    capsys,
) -> None:
    """Проверяет повторный ввод при неправильном статусе."""
    mock_load_transactions.return_value = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "description": "Перевод организации",
            "operationAmount": {
                "currency": {
                    "code": "RUB",
                }
            },
        }
    ]

    user_answers = [
        "1",
        "test",
        "executed",
        "нет",
        "нет",
        "нет",
    ]

    with patch(
        "builtins.input",
        side_effect=user_answers,
    ):
        main()

    captured = capsys.readouterr()

    assert 'Статус операции "TEST" недоступен.' in captured.out
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured.out


@patch("main.load_transactions")
def test_main_empty_result(
    mock_load_transactions: Mock,
    capsys,
) -> None:
    """Проверяет вывод сообщения при пустой выборке."""
    mock_load_transactions.return_value = [
        {
            "id": 1,
            "state": "CANCELED",
            "date": "2023-01-01T10:00:00",
            "description": "Перевод организации",
            "operationAmount": {
                "currency": {
                    "code": "RUB",
                }
            },
        }
    ]

    user_answers = [
        "1",
        "EXECUTED",
        "нет",
        "нет",
        "нет",
    ]

    with patch(
        "builtins.input",
        side_effect=user_answers,
    ):
        main()

    captured = capsys.readouterr()

    assert "Не найдено ни одной транзакции" in captured.out


@patch("main.load_transactions")
def test_main_status_lowercase(
    mock_load_transactions: Mock,
    capsys,
) -> None:
    """Проверяет ввод статуса в нижнем регистре."""
    mock_load_transactions.return_value = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "description": "Перевод организации",
            "operationAmount": {
                "currency": {
                    "code": "RUB",
                }
            },
        }
    ]

    user_answers = [
        "1",
        "executed",
        "нет",
        "нет",
        "нет",
    ]

    with patch(
        "builtins.input",
        side_effect=user_answers,
    ):
        main()

    captured = capsys.readouterr()

    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured.out


@patch("main.load_transactions")
def test_main_invalid_menu(
    mock_load_transactions: Mock,
    capsys,
) -> None:
    """Проверяет неправильный пункт главного меню."""
    with patch(
        "builtins.input",
        return_value="10",
    ):
        main()

    captured = capsys.readouterr()

    assert "Некорректный пункт меню." in captured.out

    mock_load_transactions.assert_not_called()
