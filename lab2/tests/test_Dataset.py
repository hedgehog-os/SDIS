class DummyChart:
    def __init__(self, chart_id, title, chart_type, data):
        self.chart_id = chart_id
        self.title = title
        self.chart_type = chart_type
        self.data = data

class DummyReport:
    def __init__(self):
        self.charts = []

import pytest
from metadata_and_analitics.Dataset import DataSet

@pytest.fixture
def dataset():
    return DataSet(
        dataset_id=1,
        name="Температурные измерения",
        source="Сенсор A",
        records=[
            {"month": "Январь", "temperature": -5},
            {"month": "Февраль", "temperature": -3},
            {"month": "Март", "temperature": 2}
        ]
    )
def test_initial_state(dataset):
    assert dataset.dataset_id == 1
    assert dataset.name == "Температурные измерения"
    assert dataset.source == "Сенсор A"
    assert len(dataset.records) == 3

def test_add_record(dataset):
    new_record = {"month": "Апрель", "temperature": 10}
    dataset.add_record(new_record)
    assert new_record in dataset.records

def test_remove_record(dataset):
    dataset.remove_record(1)
    assert len(dataset.records) == 2
    assert dataset.records[0]["month"] == "Январь"

def test_get_record_count(dataset):
    assert dataset.get_record_count() == 3

def test_get_fields(dataset):
    fields = dataset.get_fields()
    assert "month" in fields
    assert "temperature" in fields

def test_filter_records(dataset):
    filtered = dataset.filter_records("temperature", -3)
    assert filtered == [{"month": "Февраль", "temperature": -3}]

def test_summarize(dataset):
    summary = dataset.summarize()
    assert "DataSet #1 — Температурные измерения" in summary
    assert "Источник: Сенсор A" in summary
    assert "Записей: 3" in summary
    assert "Поля: month, temperature" in summary or "Поля: temperature, month" in summary

def test_to_dict(dataset):
    data = dataset.to_dict()
    assert data["dataset_id"] == 1
    assert data["name"] == "Температурные измерения"
    assert data["records"] == dataset.records

def test_contains_field_true(dataset):
    assert dataset.contains_field("temperature") is True

def test_contains_field_false(dataset):
    assert dataset.contains_field("humidity") is False

def test_export_as_csv_text(dataset):
    csv = dataset.export_as_csv_text()
    assert "month,temperature" in csv or "temperature,month" in csv
    assert "Январь" in csv
    assert "-5" in csv

def test_export_as_csv_text_empty():
    empty = DataSet(2, "Пустой", "Источник", [])
    assert empty.export_as_csv_text() == "Нет данных для экспорта."

def test_aggregate_field(dataset):
    agg = dataset.aggregate_field("temperature")
    assert agg["sum"] == -6
    assert agg["avg"] == -2.0
    assert agg["max"] == 2
    assert agg["min"] == -5

def test_aggregate_field_non_numeric():
    ds = DataSet(3, "Текстовые", "Источник", [{"a": "x"}, {"a": "y"}])
    agg = ds.aggregate_field("a")
    assert agg == {"sum": 0, "avg": 0, "max": 0, "min": 0}

def test_to_chart_data(dataset):
    chart_data = dataset.to_chart_data("month", "temperature")
    assert chart_data == {"Январь": -5, "Февраль": -3, "Март": 2}

