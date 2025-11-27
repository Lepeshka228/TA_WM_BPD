import pytest
from typing import Dict, Any, List
from reports.base import ReportBase


def test_report_base_cannot_be_instantiated():
    """ Для абстрактного класса нельзя создать объект """
    with pytest.raises(TypeError):
        ReportBase()


class DummyReport(ReportBase):
    """
    Минимальная реализация для теста:
    просто возвращает имена ключей как headers и значения — как rows
    """
    def generate(self, rows: List[Dict[str, Any]]):
        headers = list(rows[0].keys()) if rows else []
        table = [list(row.values()) for row in rows]
        return headers, table


def test_dummy_report_generate():
    """ проверка метода generate - генерации таблицы (заголовки, строки) """
    input_rows = [
        {"name": "Вова", "position": "DevOps", "performance": 4.5},
        {"name": "Петя", "position": "DataScientist", "performance": 3.2}
    ]

    report = DummyReport()
    headers, table = report.generate(input_rows)

    assert headers == ["name", "position", "performance"]
    assert table == [
        ["Вова", "DevOps", 4.5],
        ["Петя", "DataScientist", 3.2]
    ]


def test_dummy_report_empty_input():
    """ проверка пустого ввода, выводится пустая таблица"""
    report = DummyReport()
    headers, table = report.generate([])

    assert headers == []
    assert table == []
