# Transaction Analysis

Курсовая работа на основе Bank Project: анализ банковских операций из Excel.
Код и история предыдущих заданий сохранены. Основная ветка разработки — `develop`,
каждая задача выполняется в отдельной feature-ветке.

## Данные

`data/operations.xlsx` — доступная [копия учебной выгрузки](https://github.com/ku93/cours_1/blob/taskk1/data/operations.xlsx):
6705 операций за 2018–2021 годы. Исходная ссылка урока на Google Диске заблокирована;
побайтовое совпадение с ней не проверено.

`load_operations` использует существующий `load_transactions_excel`, сохраняет
русские названия столбцов и преобразует даты. Старые загрузчики JSON, CSV и Excel
продолжают работать.

## Установка и проверки

```bash
poetry install
poetry run pytest
```
