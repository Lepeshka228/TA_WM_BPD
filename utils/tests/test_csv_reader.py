import pytest
from utils.csv_reader import csv_reader


def write_csv(path, header, rows):
    """ утилита - записывает header и rows во временный csv файл """
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


@pytest.mark.parametrize(
    "header, rows, expected",
    [
        (
            ["name", "age"],
            [["Вова", "20"], ["Петя", "30"]],
            [
                {"name": "Вова", "age": "20"},
                {"name": "Петя", "age": "30"}
            ]
        ),
        (
            ["  name  ", " age "],
            [[" Вова ", " 25 "]],
            [{"name": "Вова", "age": "25"}]
        ),
        (
            ["col1", "col2"],
            [],
            []
        ),
        (
            ["a", "b"],
            [["x", None]],
            [{"a": "x", "b": None}]
        )
    ]
)
def test_csv_reader_single_file(tmp_path, header, rows, expected):
    """ Проверка корректности чтения данных """
    file = tmp_path / "file.csv"
    write_csv(file, header, rows)

    result = csv_reader([str(file)])
    assert result == expected


def test_csv_reader_multiple_files_concat(tmp_path):
    """ Проверка конкатенации нескольких файлов """

    file1 = tmp_path / "f1.csv"
    write_csv(
        file1,
        ["name", "age"],
        [["Вова", "20"]]
    )

    file2 = tmp_path / "f2.csv"
    write_csv(
        file2,
        ["name", "age"],
        [["Петя", "30"]]
    )

    result = csv_reader([str(file1), str(file2)])

    assert result == [
        {"name": "Вова", "age": "20"},
        {"name": "Петя", "age": "30"}
    ]


def test_csv_reader_different_column_order(tmp_path):
    """ Проверка корректности чтения при разном порядке колонок """

    f1 = tmp_path / "f1.csv"
    write_csv(
        f1,
        ["a", "b"],
        [["1", "2"]]
    )

    f2 = tmp_path / "f2.csv"
    write_csv(
        f2,
        ["b", "a"],
        [["3", "4"]]
    )

    result = csv_reader([str(f1), str(f2)])

    assert result == [
        {"a": "1", "b": "2"},
        {"b": "3", "a": "4"}
    ]


def test_csv_reader_handles_missing_values(tmp_path):
    """ Проверка отсутствия значения (должно преобразоваться в None)"""

    file = tmp_path / "file.csv"
    write_csv(
        file,
        ["x", "y", "z"],
        [["1", "2"], ["3", "4", "5"]]
    )

    result = csv_reader([str(file)])

    assert result == [
        {"x": "1", "y": "2", "z": None},
        {"x": "3", "y": "4", "z": "5"}
    ]
