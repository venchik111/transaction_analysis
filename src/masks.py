import logging
from pathlib import Path

logs_dir = Path(__file__).resolve().parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    logs_dir / "masks.log",
    mode="w",
    encoding="utf-8",
)

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int | str) -> str:
    """Принимает на вход номер карты и возвращает ее маску."""
    if len(str(card_number)) == 16:
        mask_card_number = str(card_number)[0:4] + " " + str(card_number)[4:6] + "** **** " + str(card_number)[-4:]

        logger.info("Маска номера карты успешно создана")
        return mask_card_number

    logger.error("Передан некорректный номер карты")
    return "it's not card number"


def get_mask_account(account_number: int | str) -> str:
    """Принимает на вход номер счета и возвращает его маску."""
    mask_account_number = "**" + str(account_number)[-4:]

    logger.info("Маска номера счета успешно создана")
    return mask_account_number
