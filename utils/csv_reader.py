import csv
from typing import List, Dict, Any

def csv_reader(filepaths: List[str]) -> List[Dict[str, Any]]:
    """
    Конкатенирует входные csv файлы(если их > 1), читает и возвращает список словарей
    (для каждой строки) - название колонки –> значение
    """
    result = []
    for filepath in filepaths:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k.strip(): (None if v == '' else (v.strip() if v is not None else v))
                             for k, v in row.items()}
                result.append(clean_row)
    return result
