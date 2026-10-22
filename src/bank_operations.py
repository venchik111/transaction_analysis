import re
from collections import Counter


def process_bank_search(
    data: list[dict],
    search: str,
) -> list[dict]:
    """Возвращает операции, содержащие строку поиска в описании."""
    result = []

    for operation in data:
        description = operation.get("description", "")

        if re.search(search, description, flags=re.IGNORECASE):
            result.append(operation)

    return result


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
