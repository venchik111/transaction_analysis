import logging
from functools import wraps
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from src.utils import BASE_DIR

logger = logging.getLogger(__name__)


def log(filename: str | None = None):
    """Логирует выполнение функции в файл или консоль."""

    def decorator(func):
        """Принимает функцию, которую необходимо декорировать."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Выполняет функцию и записывает информацию о ее работе."""

            def write_log(message: str) -> None:
                """Записывает сообщение в файл или выводит в консоль."""
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)

            write_log(f"Начало выполнения функции {func.__name__}")

            try:
                result = func(*args, **kwargs)

                write_log(f"Функция {func.__name__} успешно выполнена. " f"Результат: {result}")

                return result

            except Exception as error:
                write_log(
                    f"Функция {func.__name__} завершилась с ошибкой "
                    f"{type(error).__name__}. "
                    f"Входные параметры: {args}, {kwargs}"
                )
                raise

            finally:
                write_log(f"Конец выполнения функции {func.__name__}")

        return wrapper

    return decorator


def save_report(filename: str | Path | None = None) -> Callable:
    """Сохраняет результат функции-отчета в Excel."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> pd.DataFrame:
            result = func(*args, **kwargs)
            file_path = Path(filename) if filename else BASE_DIR / "reports" / "spending_by_category.xlsx"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            result.to_excel(file_path, index=False)
            logger.info("Отчет сохранен в %s", file_path)
            return result

        return wrapper

    return decorator
