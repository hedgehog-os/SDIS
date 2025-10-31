from datetime import datetime

class DummyDocument:
    def __init__(self, document_id):
        self.document_id = document_id
        self.tags = []

class DummyMetadata:
    def __init__(self):
        self.tags = []

class DummyInsight:
    def __init__(self, description):
        self.description = description

class DummyComment:
    def __init__(self, comment_id, document_id, user_id, content, posted_at):
        self.comment_id = comment_id
        self.document_id = document_id
        self.user_id = user_id
        self.content = content
        self.posted_at = posted_at

class DummyReport:
    def __init__(self, report_id, author_id):
        self.report_id = report_id
        self.author_id = author_id
        self.comments = []
import pytest
from metadata_and_analitics.Tag import Tag

@pytest.fixture
def tag():
    return Tag(tag_id=1, name="важное", category="priority")
def test_apply_to_document(tag):
    doc = DummyDocument(document_id=101)
    tag.apply_to_document(doc)
    assert doc in tag.applied_to
    assert "важное" in doc.tags

def test_remove_from_document(tag):
    doc = DummyDocument(document_id=102)
    tag.apply_to_document(doc)
    tag.remove_from_document(doc)
    assert doc not in tag.applied_to
    assert "важное" not in doc.tags

def test_is_applied_to(tag):
    doc = DummyDocument(document_id=103)
    tag.apply_to_document(doc)
    assert tag.is_applied_to(doc) is True

def test_get_document_ids(tag):
    doc1 = DummyDocument(document_id=201)
    doc2 = DummyDocument(document_id=202)
    tag.apply_to_documents([doc1, doc2])
    assert tag.get_document_ids() == [201, 202]

def test_to_dict(tag):
    doc = DummyDocument(document_id=301)
    tag.apply_to_document(doc)
    data = tag.to_dict()
    assert data["tag_id"] == 1
    assert data["name"] == "важное"
    assert data["category"] == "priority"
    assert data["applied_to"] == [301]

def test_format_for_display(tag):
    doc = DummyDocument(document_id=401)
    tag.apply_to_document(doc)
    output = tag.format_for_display()
    assert "Тег #1: важное" in output
    assert "(priority)" in output
    assert "1 документов" in output

def test_matches_category_true(tag):
    assert tag.matches_category("priority") is True

def test_matches_category_false(tag):
    assert tag.matches_category("status") is False

def test_apply_to_documents(tag):
    doc1 = DummyDocument(document_id=501)
    doc2 = DummyDocument(document_id=502)
    tag.apply_to_documents([doc1, doc2])
    assert doc1 in tag.applied_to
    assert doc2 in tag.applied_to

def test_filter_documents_by_category_match(tag):
    doc = DummyDocument(document_id=601)
    tag.apply_to_document(doc)
    filtered = tag.filter_documents_by_category("priority")
    assert filtered == [doc]

def test_filter_documents_by_category_mismatch(tag):
    doc = DummyDocument(document_id=602)
    tag.apply_to_document(doc)
    filtered = tag.filter_documents_by_category("workflow")
    assert filtered == []

def test_visualize_distribution(tag):
    for i in range(5):
        tag.apply_to_document(DummyDocument(document_id=700 + i))
    output = tag.visualize_distribution()
    assert "важное (priority)" in output
    assert "(5 документов)" in output
    assert output.count("|") == 5

def test_apply_to_metadata(tag):
    metadata = DummyMetadata()
    tag.apply_to_metadata(metadata)
    assert "важное" in metadata.tags

def test_is_relevant_to_insight_true(tag):
    insight = DummyInsight(description="Это важное наблюдение")
    assert tag.is_relevant_to_insight(insight) is True

def test_is_relevant_to_insight_false(tag):
    insight = DummyInsight(description="Ничего важного нет")
    tag.name = "приоритет"
    assert tag.is_relevant_to_insight(insight) is False
