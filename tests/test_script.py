from unittest.mock import patch, MagicMock
import pytest
from script import script
from utils.csv_reader import csv_reader
import csv


fake_report = MagicMock()
# определяем метод generate
fake_report.generate.return_value = (["col1", "col2"], [["val1", "val2"]])


def test_script_success(tmp_path, capsys):
    """ Проверка работоспособности генерации отчета """
    # создаём тестовый csv
    file = tmp_path / "data.csv"
    file.write_text("a,b\nx,1\n", encoding="utf-8")

    with patch("script.REPORT_REGISTRY", {"fake": lambda: fake_report}):
        script(["--files", str(file), "--report", "fake"])

    captured = capsys.readouterr()
    assert "val1" in captured.out
    assert "val2" in captured.out
    fake_report.generate.assert_called_once()  # проверяем вызов generate


def test_script_file_not_found(capsys):
    """ Проверка несуществующего csv файла """
    with patch("script.REPORT_REGISTRY", {"fake": lambda: fake_report}):
        script(["--files", "no_file.csv", "--report", "fake"])

    captured = capsys.readouterr()
    assert "файл не найден" in captured.err.lower()


def test_script_invalid_report(tmp_path, capsys):
    """
    Проверка некорректного названия отчета - должно вываливаться
    SystemExit, т.к. argparse там тестирует
    """
    file = tmp_path / "data.csv"
    file.write_text("a,b\nx,1\n")

    with patch("script.REPORT_REGISTRY", {'smthng': lambda: fake_report}):
        with pytest.raises(SystemExit) as e:
            script(["--files", str(file), "--report", "nonexistent"])

    assert e.value.code == 2    # код ошибки


def test_script_csv_error(tmp_path, capsys):
    """ Ошибка чтения csv """
    file = tmp_path / "data.csv"
    file.write_text("a,b\nx,1\n")

    with patch("script.csv_reader", side_effect=csv.Error("bad csv")):
        with patch("script.REPORT_REGISTRY", {"fake": lambda: fake_report}):
            script(["--files", str(file), "--report", "fake"])

    captured = capsys.readouterr()
    assert "ошибка при чтении файлов" in captured.err.lower()
