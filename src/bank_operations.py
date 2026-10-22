import re
from collections import Counter


def process_bank_search(
    data: list[dict],
    search: str,
    fields: tuple[str, ...] = ("description",),
) -> list[dict]:
    """Возвращает операции, содержащие строку поиска в указанных полях."""

    def matches(operation: dict) -> bool:
        for field in fields:
            value = operation.get(field)
            text = value if isinstance(value, str) else ""
            if re.search(search, text, flags=re.IGNORECASE):
                return True
        return False

    return list(filter(matches, data))


def process_bank_operations(
    data: list[dict],
    categories: list[str],
) -> dict[str, int]:
    """Возвращает количество операций по заданным категориям."""
    descriptions = [operation.get("description", "") for operation in data]

    counter = Counter(descriptions)

    result = {}

    for category in categories:
        result[category] = counter.get(category, 0)

    return result
