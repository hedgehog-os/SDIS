from datetime import datetime

class DummyDocument:
    def __init__(self, document_id):
        self.document_id = document_id
        self.statistics = None

class DummyRevision:
    def __init__(self, document_id):
        self.document_id = document_id

class DummyMetadata:
    def __init__(self, document_id):
        self.document_id = document_id

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
from metadata_and_analitics.Statistics import Statistics

@pytest.fixture
def stats():
    return Statistics(document_id=1, views=5, edits=2, comments=1)
def test_increment_views(stats):
    stats.increment_views(3)
    assert stats.views == 8

def test_increment_edits(stats):
    stats.increment_edits(2)
    assert stats.edits == 4

def test_increment_comments(stats):
    stats.increment_comments(1)
    assert stats.comments == 2

def test_increment_negative(stats):
    stats.increment_views(-5)
    stats.increment_edits(-1)
    stats.increment_comments(-2)
    assert stats.views == 5
    assert stats.edits == 2
    assert stats.comments == 1

def test_reset_statistics(stats):
    stats.reset_statistics()
    assert stats.views == 0
    assert stats.edits == 0
    assert stats.comments == 0

def test_get_summary(stats):
    summary = stats.get_summary()
    assert "Статистика по документу #1" in summary
    assert "Просмотры: 5" in summary
    assert "Правки: 2" in summary
    assert "Комментарии: 1" in summary

def test_to_dict(stats):
    data = stats.to_dict()
    assert data == {"document_id": 1, "views": 5, "edits": 2, "comments": 1}

def test_is_active_false(stats):
    assert stats.is_active() is False

def test_is_active_true(stats):
    stats.increment_views(10)
    assert stats.is_active() is True

def test_link_to_document(stats):
    doc = DummyDocument(document_id=1)
    stats.link_to_document(doc)
    assert doc.statistics == stats

def test_link_to_document_mismatch(stats):
    doc = DummyDocument(document_id=99)
    stats.link_to_document(doc)
    assert doc.statistics is None

def test_update_from_revision(stats):
    rev = DummyRevision(document_id=1)
    stats.update_from_revision(rev)
    assert stats.edits == 3

def test_reflect_metadata_activity(stats):
    meta = DummyMetadata(document_id=1)
    stats.reflect_metadata_activity(meta)
    assert stats.views == 6

def test_compare_to(stats):
    other = Statistics(document_id=1, views=3, edits=1, comments=2)
    diff = stats.compare_to(other)
    assert diff == {"views_diff": 2, "edits_diff": 1, "comments_diff": -1}

def test_visualize_activity(stats):
    output = stats.visualize_activity()
    assert "Активность документа #1" in output
    assert "Просмотры: |||||" in output
    assert "Правки: ||" in output
    assert "Комментарии: |" in output
