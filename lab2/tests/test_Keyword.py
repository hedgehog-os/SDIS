import pytest
from metadata_and_analitics.Keyword import Keyword

@pytest.fixture(scope="function")
def keyword():
    return Keyword(word="температура", relevance_score=0.6)
class DummyRevision:
    def __init__(self, notes=None, change_history=None):
        self.notes = notes
        self.change_history = change_history or []

class DummyComment:
    def __init__(self, content):
        self.content = content

class DummyDocument:
    def __init__(self, title, tags=None, revisions=None, comments=None):
        self.title = title
        self.tags = tags or []
        self.revisions = revisions or []
        self.comments = comments or []
        self.keywords = []

class DummyInsight:
    def __init__(self, insight_id, description):
        self.insight_id = insight_id
        self.description = description
def test_boost_score_positive(keyword):
    keyword.boost_score(0.2)
    assert keyword.relevance_score == 0.8

def test_boost_score_negative(keyword):
    keyword.boost_score(-1)
    assert keyword.relevance_score == 0.6  # не должно измениться

def test_reduce_score_positive(keyword):
    keyword.reduce_score(0.3)
    assert keyword.relevance_score == 0.3

def test_reduce_score_below_zero(keyword):
    keyword.reduce_score(10)
    assert keyword.relevance_score == 0.0

def test_is_significant_above_threshold(keyword):
    assert keyword.is_significant(0.5) is True

def test_is_significant_below_threshold(keyword):
    keyword.relevance_score = 0.4
    assert keyword.is_significant(0.5) is False

def test_format_for_display(keyword):
    keyword.relevance_score = 0.4
    assert keyword.format_for_display() == "температура (релевантность: 0.40)"

def test_to_dict(keyword):
    keyword.relevance_score = 0.4
    assert keyword.to_dict() == {"word": "температура", "relevance_score": 0.4}



def test_matches_false(keyword):
    assert keyword.matches("Давление и влажность") is False


def test_is_used_in_document_tags(keyword):
    doc = DummyDocument(title="Документ", tags=["давление", "температура"])
    assert keyword.is_used_in_document(doc) is True

def test_is_used_in_document_notes(keyword):
    rev = DummyRevision(notes="Температура была нестабильной")
    doc = DummyDocument(title="Документ", revisions=[rev])
    assert keyword.is_used_in_document(doc) is True

def test_is_used_in_document_change_history(keyword):
    rev = DummyRevision(change_history=["Изменена температура"])
    doc = DummyDocument(title="Документ", revisions=[rev])
    assert keyword.is_used_in_document(doc) is True

def test_is_used_in_document_comments(keyword):
    comment = DummyComment(content="Температура выше нормы")
    doc = DummyDocument(title="Документ", comments=[comment])
    assert keyword.is_used_in_document(doc) is True

def test_link_to_document(keyword):
    doc = DummyDocument(title="Документ")
    keyword.link_to_document(doc)
    assert keyword in doc.keywords

def test_link_to_document_no_duplicate(keyword):
    doc = DummyDocument(title="Документ")
    doc.keywords.append(keyword)
    keyword.link_to_document(doc)
    assert doc.keywords.count(keyword) == 1

def test_is_used_in_insight_true(keyword):
    insight = DummyInsight(insight_id=1, description="Температура влияет на результат")
    assert keyword.is_used_in_insight(insight) is True

def test_is_used_in_insight_false(keyword):
    insight = DummyInsight(insight_id=2, description="Давление и влажность")
    assert keyword.is_used_in_insight(insight) is False

def test_link_to_insight(keyword):
    insight = DummyInsight(insight_id=3, description="Температура важна")
    keyword.link_to_insight(insight)
    assert hasattr(keyword, "linked_insights")
    assert 3 in keyword.linked_insights

def test_link_to_insight_no_duplicate(keyword):
    insight = DummyInsight(insight_id=4, description="Температура важна")
    keyword.link_to_insight(insight)
    keyword.link_to_insight(insight)
    assert keyword.linked_insights.count(4) == 1
