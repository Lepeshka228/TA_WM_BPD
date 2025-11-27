# класс отчета для performance - наследник ReportBase, обязан реализовать generate
from collections import defaultdict
from typing import List, Dict, Any, Tuple

from reports.base import ReportBase


class PerformanceReport(ReportBase):
    """
    Отчет по столбцу performance для каждого значения positions

    Группирует по position и считает среднее арифметическое по performance.
    Результат сортируется по убыванию среднего performance.

    Возвращает колонки:
        # - порядковый номер (искусственный)
        position - название позиции
        performance - ср. знач. performance для каждой позиции
    """
    def generate(self, rows: List[Dict[str, Any]]) -> Tuple[List[str], List[List[Any]]]:
        agg = defaultdict(lambda: [0.0, 0])

        for r in rows:
            pos = r.get('position', None)
            perf = r.get('performance', None)

            # если нет значений -> пропускаем
            if perf is None or pos is None:
                continue

            # пробуем преобразовать в float, если нет -> пропускаем
            try:
                perf = float(perf)
            except (ValueError, TypeError):
                continue

            # заносим значения для данной позиции
            agg[pos][0] += perf
            agg[pos][1] += 1

        # формируем список [(позиция, ср. знач.), ...]
        results = []
        for pos, (sum, cnt) in agg.items():
            if cnt == 0:
                continue
            mean = round(sum / cnt, 2)
            results.append((pos, mean))

        # сортируем по убыванию
        results.sort(key=lambda x: x[1], reverse=True)

        # формируем строки таблицы (mean с 2 знаками аосле запятой)
        table_rows = []
        for id, (pos, mean) in enumerate(results, start=1):
            table_rows.append([id, pos, mean])
        headers = ['#', 'position', 'performance']
        return headers, table_rows
