from datetime import datetime

class DummyComment:
    def __init__(self, comment_id, document_id, user_id, content, posted_at):
        self.comment_id = comment_id
        self.document_id = document_id
        self.user_id = user_id
        self.content = content
        self.posted_at = posted_at

class DummyReport:
    def __init__(self, report_id=10, author_id=99):
        self.report_id = report_id
        self.author_id = author_id
        self.comments = []
import pytest
from metadata_and_analitics.Insight import Insight

@pytest.fixture
def insight():
    return Insight(
        insight_id=1,
        description="Этот инсайт связан с несколькими важными документами.",
        related_documents=[101, 102, 103]
    )
def test_initial_state(insight):
    assert insight.insight_id == 1
    assert "важными документами" in insight.description
    assert insight.related_documents == [101, 102, 103]

def test_add_related_document(insight):
    insight.add_related_document(104)
    assert 104 in insight.related_documents

def test_add_related_document_no_duplicate(insight):
    insight.add_related_document(102)
    assert insight.related_documents.count(102) == 1

def test_remove_related_document(insight):
    insight.remove_related_document(101)
    assert 101 not in insight.related_documents

def test_is_related_to_true(insight):
    assert insight.is_related_to(102) is True

def test_is_related_to_false(insight):
    assert insight.is_related_to(999) is False

def test_summarize_short(insight):
    summary = insight.summarize(max_length=200)
    assert summary == insight.description

def test_summarize_truncated(insight):
    summary = insight.summarize(max_length=10)
    assert summary.startswith(insight.description[:10])
    assert summary.endswith("...")

def test_format_for_display(insight):
    output = insight.format_for_display()
    assert "Insight #1" in output
    assert "Связанные документы: 101, 102, 103" in output

def test_get_related_count(insight):
    assert insight.get_related_count() == 3

def test_to_dict(insight):
    data = insight.to_dict()
    assert data["insight_id"] == 1
    assert data["description"] == insight.description
    assert data["related_documents"] == [101, 102, 103]

def test_contains_keyword_true(insight):
    assert insight.contains_keyword("важными") is True

def test_contains_keyword_false(insight):
    assert insight.contains_keyword("несуществующее") is False

def test_visualize_links(insight):
    output = insight.visualize_links()
    assert "Insight #1 связан с:" in output
    assert "Документ ID: 101" in output
    assert "Документ ID: 103" in output

def test_visualize_links_empty():
    empty_insight = Insight(2, "Нет связей", [])
    assert empty_insight.visualize_links() == "Нет связанных документов."
