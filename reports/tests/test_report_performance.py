import pytest
from reports.performance import PerformanceReport


@pytest.fixture
def sample_rows():
    return [
        {"position": "Manager", "performance": 2.1, "some_title": "anything"},
        {"position": "Manager", "performance": 4.3, "some_title2": "anything_any"},
        {"position": "Developer", "some_title": 8, "performance": 3.9},
        {"position": "Developer", "performance": "4.400"},
        {"position": "Developer", "performance": None},
        {"position": "Intern", "performance": "abc"},
        {"position": None, "performance": 5},
        {"performance": "abc"},
        {"position": "Intern"},
    ]


@pytest.fixture
def generated(sample_rows):
    report = PerformanceReport()
    return report.generate(sample_rows)   # (headers, table)


def test_headers(generated):
    """ проверка заголовков """
    headers, _ = generated
    assert headers == ['#', 'position', 'performance']


@pytest.mark.parametrize("position,expected_avg", [
    ("Manager", 3.2),
    ("Developer", 4.15),
])
def test_avg_per_position(generated, position, expected_avg):
    """ проверка среднего значения """
    _, table = generated
    perf_dict = {row[1]: row[2] for row in table}
    assert perf_dict[position] == expected_avg


def test_only_expected_positions_present(generated):
    """ проверка значений позиций """
    _, table = generated
    positions = {row[1] for row in table}
    assert positions == {"Manager", "Developer"}


def test_sorted_desc_by_performance(generated):
    """ проверка сортировки по убванию """
    _, table = generated
    assert table[0][1] == "Developer"   # 4.15
    assert table[1][1] == "Manager"     # 3.2
