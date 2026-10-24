def filter_by_currency(list_of_dict: list[dict], key):
    """Выдает операции по валюте."""
    for operation in list_of_dict:
        if "operationAmount" in operation:
            currency = operation["operationAmount"]["currency"]["code"]
        else:
            currency = operation["currency_code"]

        if currency == key:
            yield operation


def transaction_descriptions(transaction: list[dict]):
    """Возвращает описание каждой операции по очереди."""
    for operation in transaction:
        yield operation["description"]


def card_number_generator(start: int, end: int):
    """Генерирует номера карт в заданном диапазоне."""
    for number in range(start, end + 1):
        card_number = f"{number:016}"

        yield (f"{card_number[:4]} " f"{card_number[4:8]} " f"{card_number[8:12]} " f"{card_number[12:]}")
