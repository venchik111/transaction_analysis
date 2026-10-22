from src import masks


def mask_account_card(number: str) -> str:
    """Маскирует номер счета или карты."""
    number_split: list[str] = number.split()

    if number.startswith("Счет"):
        number_split[-1] = masks.get_mask_account(number_split[-1])

    else:
        if len(number_split[-1]) == 16:
            number_split[-1] = masks.get_mask_card_number(number_split[-1])

        else:
            number_split[-1] = masks.get_mask_card_number(number_split[-1])
            number_split.pop(0)

    mask_number = " ".join(number_split)

    return mask_number


def get_date(date: str) -> str:
    """Принимает дату и возвращает ее в формате ДД.ММ.ГГГГ."""
    try:
        if len(date) >= 11 and date[10] == "T":
            return f"{date[8:10]}." f"{date[5:7]}." f"{date[0:4]}"

    except (IndexError, TypeError):
        pass

    return "wrong data format"
