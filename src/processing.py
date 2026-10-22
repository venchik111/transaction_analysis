from datetime import datetime


def filter_by_state(
    list_of_dicts: list[dict],
    filter_state: str = "EXECUTED",
) -> list[dict]:
    """Фильтрует список операций по статусу."""
    filtered_operations = []

    for item in list_of_dicts:
        if item.get("state") == filter_state:
            filtered_operations.append(item)

    return filtered_operations


def sort_by_date(
    list_of_dicts: list[dict],
    reverse: bool = True,
) -> list[dict]:
    """Сортирует список операций по дате."""

    def get_date(item: dict):
        date = item.get("date")

        if date:
            return datetime.fromisoformat(date)

        return datetime.min

    return sorted(
        list_of_dicts,
        key=get_date,
        reverse=reverse,
    )
