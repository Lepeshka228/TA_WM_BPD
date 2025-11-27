# Описание
ТЗ: https://docs.google.com/document/d/1QwinJt_NBghu9O3qBQ7CvvjW7RykHizJjmrZuRwa37M/edit?tab=t.0#heading=h.or54d8e34zbk

Скрипт script.py принимает два аргумента `--files` с указанными путями к csv файлам и `--report` с указанным названием отчета
<img width="657" height="214" alt="Снимок экрана 2025-11-27 в 22 36 10" src="https://github.com/user-attachments/assets/cd373768-61d2-4823-8ec7-f94743f475b8" />

и формирует отчет в виде таблице в cli
<img width="1027" height="221" alt="Снимок экрана 2025-11-27 в 22 37 40" src="https://github.com/user-attachments/assets/3a4419cb-53bc-439c-83ca-70eb108e56f3" />

# Особенности реализация
В архитектуру заложена возможность добавления новых отчётов, для этого нужно определить новый ключ (он будет значением для --report) 
в REPORT_REGISTRY (`./reports/__init__.py`), значение которого - класс, реализующий логику обработки данных для данного отчета. Каждый такой класс наследует 
ABC ReportBase и обязан реализовать метод generate

покрытие тестами 98%
<img width="1265" height="615" alt="Снимок экрана 2025-11-27 в 22 38 51" src="https://github.com/user-attachments/assets/2ab7aecc-a9e2-44bb-9487-86ea804aabfc" />


# Стек
- python3.10
  - для обработки скрипта из cli используется argparse
  - для обработки csv файлов используется модуль csv
- для вывода таблицы в cli используется библиотека tabulate
- для тестирования – pytest
