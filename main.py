import argparse
import csv
from tabulate import tabulate
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="CSV фильтрация и агрегация")
    parser.add_argument("--file", required=True, help="Путь к CSV файлу")
    parser.add_argument("--filter", nargs=3, metavar=('COLUMN', 'OPERATOR', 'VALUE'), help="Фильтрация: COLUMN OPERATOR VALUE")
    parser.add_argument("--aggregate", nargs=2, metavar=('COLUMN', 'FUNCTION'), help="Агрегация: COLUMN FUNCTION (avg|min|max)")
    return parser.parse_args()

def read_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def apply_filter(data, column, operator, value):
    if column not in data[0]:
        sys.exit(f"Колонка '{column}' не найдена")

    try:
        value_num = float(value)
        is_numeric = True
    except ValueError:
        is_numeric = False

    def match(row):
        val = row[column]
        if is_numeric:
            val = float(val)
            if operator == '>': return val > value_num
            elif operator == '<': return val < value_num
            elif operator == '=': return val == value_num
        else:
            if operator == '=': return val == value
            else: sys.exit("Для текстовых колонок только оператор '='")
        return False

    return list(filter(match, data))

def apply_aggregation(data, column, func):
    try:
        values = [float(row[column]) for row in data]
    except KeyError:
        sys.exit(f"Колонка '{column}' не найдена")
    except ValueError:
        sys.exit(f"Колонка '{column}' содержит нечисловые значения")

    if func == "avg":
        result = sum(values) / len(values) if values else 0
    elif func == "min":
        result = min(values)
    elif func == "max":
        result = max(values)
    else:
        sys.exit("Функция агрегации должна быть одной из: avg, min, max")

    print(f"{func.upper()} по колонке '{column}': {result}")

def main():
    args = parse_arguments()
    data = read_csv(args.file)

    if args.filter:
        column, op, value = args.filter
        if op not in ['>', '<', '=']:
            sys.exit("Допустимые операторы фильтрации: >, <, =")
        data = apply_filter(data, column, op, value)
        print(tabulate(data, headers="keys", tablefmt="grid"))

    elif args.aggregate:
        column, func = args.aggregate
        apply_aggregation(data, column, func.lower())

    else:
        print(tabulate(data, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()