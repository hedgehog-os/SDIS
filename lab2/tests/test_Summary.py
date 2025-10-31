from datetime import datetime, timedelta

class DummyReport:
    def __init__(self, report_id, title, author_id=1):
        self.report_id = report_id
        self.title = title
        self.author_id = author_id
        self.comments = []
        self.summaries = []

class DummyInsight:
    def __init__(self, insight_id, description):
        self.insight_id = insight_id
        self.description = description

class DummyKeyword:
    def __init__(self, word):
        self.word = word

class DummyChart:
    def __init__(self, chart_id, title):
        self.chart_id = chart_id
        self.title = title

class DummyDocument:
    def __init__(self, document_id, title):
        self.document_id = document_id
        self.title = title
import pytest
from metadata_and_analitics.Summary import Summary

@pytest.fixture
def summary():
    return Summary(
        summary_id=1,
        content="Инсайт 42: температура важна. Диаграмма: График роста. Документ #101: Протокол эксперимента.",
        generated_at=datetime.now() - timedelta(minutes=30)
    )
def test_update_content(summary):
    old_time = summary.generated_at
    summary.update_content("Новая сводка по отчёту.")
    assert summary.content == "Новая сводка по отчёту."
    assert summary.generated_at > old_time

def test_get_summary_excerpt_short(summary):
    excerpt = summary.get_summary_excerpt(200)
    assert excerpt == summary.content

def test_get_summary_excerpt_truncated(summary):
    excerpt = summary.get_summary_excerpt(10)
    assert excerpt.startswith(summary.content[:10])
    assert excerpt.endswith("...")

def test_is_recent_true(summary):
    assert summary.is_recent(threshold_minutes=60) is True

def test_is_recent_false(summary):
    summary.generated_at = datetime.now() - timedelta(hours=2)
    assert summary.is_recent(threshold_minutes=60) is False

def test_format_for_display(summary):
    report = DummyReport(report_id=1, title="Итоговый отчёт")
    summary.link_to_report(report)
    output = summary.format_for_display()
    assert f"Сводка #1" in output
    assert "Итоговый отчёт" in output
    assert "Содержание:" in output

def test_link_to_report(summary):
    report = DummyReport(report_id=1, title="Отчёт")
    summary.link_to_report(report)
    assert summary.report == report
    assert summary in report.summaries

def test_to_dict(summary):
    report = DummyReport(report_id=1, title="Отчёт")
    summary.link_to_report(report)
    data = summary.to_dict()
    assert data["summary_id"] == 1
    assert data["content"] == summary.content
    assert data["report_id"] == 1
    assert isinstance(data["generated_at"], str)

def test_extract_insights(summary):
    insights = [
        DummyInsight(42, "температура важна"),
        DummyInsight(99, "давление не влияет")
    ]
    found = summary.extract_insights(insights)
    assert len(found) == 1
    assert found[0].insight_id == 42

def test_extract_keywords(summary):
    keywords = [DummyKeyword("температура"), DummyKeyword("влажность")]
    found = summary.extract_keywords(keywords)
    assert len(found) == 1
    assert found[0].word == "температура"

def test_referenced_documents(summary):
    docs = [
        DummyDocument(101, "Протокол эксперимента"),
        DummyDocument(202, "Описание условий")
    ]
    found = summary.referenced_documents(docs)
    assert len(found) == 1
    assert found[0].document_id == 101

def test_semantic_map(summary):
    insights = [DummyInsight(42, "температура важна")]
    keywords = [DummyKeyword("температура")]
    charts = [DummyChart(1, "График роста")]
    docs = [DummyDocument(101, "Протокол эксперимента")]
    result = summary.semantic_map(insights, keywords, charts, docs)
    assert result == {
        "insights": [42],
        "keywords": ["температура"],
        "charts": [1],
        "documents": [101]
    }
