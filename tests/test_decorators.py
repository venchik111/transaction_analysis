import pytest

from src.decorators import log


def test_log_console_success(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "Начало выполнения функции add" in captured.out
    assert "Функция add успешно выполнена. Результат: 5" in captured.out
    assert "Конец выполнения функции add" in captured.out


def test_log_console_error(capsys):
    @log()
    def division(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        division(10, 0)

    captured = capsys.readouterr()

    assert "Начало выполнения функции division" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "Входные параметры: (10, 0), {}" in captured.out
    assert "Конец выполнения функции division" in captured.out


def test_log_file_success(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(str(log_file))
    def add(a, b):
        return a + b

    result = add(5, 10)
    log_text = log_file.read_text(encoding="utf-8")

    assert result == 15
    assert "Начало выполнения функции add" in log_text
    assert "Функция add успешно выполнена. Результат: 15" in log_text
    assert "Конец выполнения функции add" in log_text


def test_log_file_error(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(str(log_file))
    def division(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        division(10, 0)

    log_text = log_file.read_text(encoding="utf-8")

    assert "Начало выполнения функции division" in log_text
    assert "ZeroDivisionError" in log_text
    assert "Входные параметры: (10, 0), {}" in log_text
    assert "Конец выполнения функции division" in log_text
