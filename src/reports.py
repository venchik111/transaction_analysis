import logging
from datetime import datetime

import pandas as pd

from src.decorators import save_report
from src.utils import parse_dates

logger = logging.getLogger(__name__)


@save_report()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: str | None = None,
) -> pd.DataFrame:
    """Возвращает траты по категории за последние три месяца."""
    end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    end_date = pd.Timestamp(end_date).normalize()
    start_date = end_date - pd.DateOffset(months=3)
    dates = parse_dates(transactions["Дата операции"]).dt.normalize()
    result = transactions.loc[
        (dates >= start_date)
        & (dates <= end_date)
        & (transactions["Категория"] == category)
        & (transactions["Статус"] == "OK")
        & (transactions["Сумма платежа"] < 0)
    ].copy()

    logger.info("Сформирован отчет по категории %s: %s операций", category, len(result))
    return result
