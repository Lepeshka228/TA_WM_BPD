# Реестр отчётов. Возможные значения для отчета - ключ REPORT_REGISTRY,
# значение REPORT_REGISTRY - класс, оставляющий отчет

from .performance import PerformanceReport

REPORT_REGISTRY = {
    "performance": PerformanceReport
}
