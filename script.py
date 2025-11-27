import argparse
import csv
import sys
from typing import List
from tabulate import tabulate

from utils.csv_reader import csv_reader
from reports import REPORT_REGISTRY

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Makes a report based on csv "
                                                 "files (or 1 file) and outputs it to the CLI")
    parser.add_argument("--files",
                        required=True,
                        nargs="+",
                        help="list or 1 csv file to process")
    parser.add_argument("--report",
                        required=True,
                        choices=REPORT_REGISTRY.keys(),
                        help="report name")
    return parser.parse_args(argv)


def script(argv: List[str]) -> None:
    args = parse_args(argv)

    try:
        rows = csv_reader(args.files)
    except FileNotFoundError as e:
        print(f"Ошибка, файл не найден – {e}", file=sys.stderr)
        return None
    except csv.Error as e:
        print(f"Ошибка при чтении файлов: {e}", file=sys.stderr)
        return None

    report_opt = REPORT_REGISTRY.get(args.report)
    if report_opt is None:
        print(f"Неизвестный вариант отчёта {args.report}", file=sys.stderr)
        return None

    report = report_opt()
    headers, table_rows = report.generate(rows)

    print(tabulate(table_rows, headers=headers, tablefmt="pipe", showindex=False, floatfmt=".2f"))
    return None

if __name__ == "__main__":
    script(sys.argv[1:])