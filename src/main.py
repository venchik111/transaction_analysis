from src.reports import spending_by_category
from src.services import simple_search
from src.utils import BASE_DIR, load_operations, setup_logging
from src.views import main_page


def main() -> None:
    """Запускает примеры работы с банковскими операциями."""
    setup_logging()
    print("1. Главная")
    print("2. Простой поиск")
    print("3. Траты по категории")
    choice = input("Выберите пункт меню: ")

    if choice == "1":
        date = input("Введите дату и время (YYYY-MM-DD HH:MM:SS): ")
        print(main_page(date))
    elif choice == "2":
        transactions = load_operations(BASE_DIR / "data" / "operations.xlsx")
        search = input("Введите строку для поиска: ")
        print(simple_search(transactions.to_dict(orient="records"), search))
    elif choice == "3":
        transactions = load_operations(BASE_DIR / "data" / "operations.xlsx")
        category = input("Введите категорию: ")
        date = input("Введите дату (YYYY-MM-DD) или нажмите Enter: ")
        report = spending_by_category(transactions, category, date or None)
        print(f"Найдено операций: {len(report)}")
        print("Отчет сохранен в reports/spending_by_category.xlsx")
    else:
        print("Некорректный пункт меню.")


if __name__ == "__main__":
    main()
