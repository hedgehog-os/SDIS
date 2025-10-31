import pytest
from metadata_and_analitics.Chart import Chart

@pytest.fixture
def chart():
    return Chart(chart_id=1, title="Температура", chart_type="line", data={"Январь": -5, "Февраль": -3})

class DummyReport:
    def __init__(self):
        self.charts = []
def test_initial_state(chart):
    assert chart.chart_id == 1
    assert chart.title == "Температура"
    assert chart.chart_type == "line"
    assert chart.data == {"Январь": -5, "Февраль": -3}

def test_invalid_chart_type():
    with pytest.raises(ValueError):
        Chart(chart_id=2, title="Неверная", chart_type="donut", data={})

def test_update_data(chart):
    new_data = {"Март": 2, "Апрель": 10}
    chart.update_data(new_data)
    assert chart.data == new_data

def test_add_data_point(chart):
    chart.add_data_point("Май", 15)
    assert chart.data["Май"] == 15

def test_remove_data_point(chart):
    chart.remove_data_point("Январь")
    assert "Январь" not in chart.data

def test_get_data_summary(chart):
    summary = chart.get_data_summary()
    assert "Январь: -5" in summary
    assert "Февраль: -3" in summary

def test_get_data_summary_empty():
    c = Chart(3, "Пустая", "bar", {})
    assert c.get_data_summary() == "Данные отсутствуют."

def test_get_chart_info(chart):
    info = chart.get_chart_info()
    assert "Диаграмма #1" in info
    assert "Тип: line" in info
    assert "Точек данных: 2" in info

def test_is_empty_true():
    c = Chart(4, "Пустая", "pie", {})
    assert c.is_empty() is True

def test_is_empty_false(chart):
    assert chart.is_empty() is False

def test_get_max_value(chart):
    assert chart.get_max_value() == -3

def test_get_min_value(chart):
    assert chart.get_min_value() == -5

def test_get_max_value_empty():
    c = Chart(5, "Нет данных", "scatter", {})
    assert c.get_max_value() is None

def test_export_as_text(chart):
    text = chart.export_as_text()
    assert "Диаграмма #1" in text
    assert "- Январь: -5" in text

def test_to_dict(chart):
    data = chart.to_dict()
    assert data["chart_id"] == 1
    assert data["title"] == "Температура"
    assert data["chart_type"] == "line"
    assert data["data"] == {"Январь": -5, "Февраль": -3}

def test_attach_to_report(chart):
    report = DummyReport()
    chart.attach_to_report(report)
    assert chart in report.charts

def test_attach_to_report_no_duplicate(chart):
    report = DummyReport()
    chart.attach_to_report(report)
    chart.attach_to_report(report)
    assert report.charts.count(chart) == 1

def test_summarize(chart):
    summary = chart.summarize()
    assert "Температура (line)" in summary
    assert "2 точек" in summary
    assert "макс: -3" in summary
    assert "мин: -5" in summary
