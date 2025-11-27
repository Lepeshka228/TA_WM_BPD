# базовый класс родитель для составления отчетов

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any


class ReportBase(ABC):
    """
    Базовый класс для всех отчётов
    """

    @abstractmethod
    def generate(self, rows: List[Dict[str, Any]]) -> Tuple[List[str], List[List[Any]]]:
        """
        Получает список записей (каждая запись — dict, ключи — названия колонок из csv)
        и возвращает кортеж (headers, rows), где:
        - headers: список строк — заголовки колонок таблицы
        - rows: список списков — строки таблицы
        """
        raise NotImplementedError
