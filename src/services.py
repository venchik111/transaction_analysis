import logging
import re

import pandas as pd

from src.bank_operations import process_bank_search
from src.utils import transactions_to_json

logger = logging.getLogger(__name__)


def simple_search(transactions: list[dict], search: str) -> str:
    """Ищет строку в описании или категории без учета регистра."""
    result = process_bank_search(transactions, re.escape(search), ("Описание", "Категория"))
    logger.info("Найдено операций: %s", len(result))
    return transactions_to_json(pd.DataFrame(result))
