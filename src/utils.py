import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
logs_dir = BASE_DIR / "logs"
logs_dir.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    logs_dir / "utils.log",
    mode="w",
    encoding="utf-8",
)

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Принимает путь до JSON-файла и возвращает список транзакций."""
    try:
        with open(file_path, encoding="utf-8") as file:
            transactions = json.load(file)

        if isinstance(transactions, list):
            logger.info("JSON-файл успешно прочитан")

            return [item for item in transactions if isinstance(item, dict) and item]

        logger.error("JSON-файл содержит не список")
        return []

    except FileNotFoundError:
        logger.error("JSON-файл не найден")
        return []

    except json.JSONDecodeError:
        logger.error("Ошибка чтения JSON-файла")
        return []


def load_transactions_csv(
    file_path: str,
) -> list[dict]:
    """Считывает финансовые операции из CSV-файла."""
    transactions = pd.read_csv(
        file_path,
        sep=";",
    )

    return transactions.to_dict(orient="records")


def read_excel_file(file_path: str | Path) -> pd.DataFrame:
    """Читает таблицу Excel, сохраняя столбцы и номера карт."""
    return pd.read_excel(file_path, dtype={"Номер карты": str})


def load_transactions_excel(
    file_path: str,
) -> list[dict]:
    """Считывает финансовые операции из XLSX-файла."""
    transactions = read_excel_file(file_path)

    return transactions.to_dict(orient="records")


def setup_logging() -> None:
    """Настраивает запись логов в файл."""
    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=logs_dir / "app.log",
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
        encoding="utf-8",
    )


def parse_dates(dates: pd.Series) -> pd.Series:
    """Разбирает русские и ISO-даты без перестановки дня и месяца."""
    iso_dates = dates.astype("string").str.match(r"^\d{4}-", na=False)
    result = pd.to_datetime(dates, format="mixed", dayfirst=True, errors="coerce")
    result.loc[iso_dates] = pd.to_datetime(dates.loc[iso_dates], format="ISO8601", errors="coerce")
    return result


def load_operations(file_path: str | Path) -> pd.DataFrame:
    """Готовит таблицу операций для курсовой на основе Excel-загрузчика."""
    transactions = read_excel_file(file_path)

    for column in ["Дата операции", "Дата платежа"]:
        if column in transactions.columns:
            transactions[column] = parse_dates(transactions[column])

    logger.info("Прочитано операций для анализа: %s", len(transactions))
    return transactions


def load_settings() -> dict:
    """Читает настройки валют и акций."""
    with open(BASE_DIR / "user_settings.json", encoding="utf-8") as file:
        settings: dict = json.load(file)
        return settings


def transactions_to_json(transactions: pd.DataFrame) -> str:
    """Преобразует таблицу в JSON с датами и пустыми значениями."""
    data = transactions.copy()

    for column in data.columns:
        if pd.api.types.is_datetime64_any_dtype(data[column]):
            data[column] = data[column].dt.strftime("%Y-%m-%d %H:%M:%S")

    return data.to_json(orient="records", force_ascii=False)
