from typing import List

import pytest
from script import parse_args

@pytest.mark.parametrize(
    "argv,expected_files,expected_report",
    [
        (["--files", "a.csv", "--report", "performance"],
         ["a.csv"], "performance"),
        (["--files", "a.csv", "b.csv", "--report", "performance"],
         ["a.csv", "b.csv"], "performance")
    ]
)
def test_parse_args_valid(argv, expected_files, expected_report):
    """ Положительные случаи, есть оба аргумента с корректными параметрами """
    args = parse_args(argv)
    assert args.files == expected_files
    assert args.report == expected_report

@pytest.mark.parametrize(
    "argv",
    [
        ["--report", "performance"],
        ["--files", "a.csv"],
        ["--files", "--report", "performance"],
        ["--files", "a.csv", "--report", "invalid_choice"]
    ]
)
def test_parse_args_invalid(argv):
    """
    Отрицательные случаи, нет аргумента --files, нет аргумента --report,
    нет файлов как параметров для --files и неверное название отчета
    """
    with pytest.raises(SystemExit):
        parse_args(argv)
