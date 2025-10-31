from datetime import datetime


class DummyDocument:
    def __init__(self, document_id):
        self.document_id = document_id
        self.revisions = []

class DummyRevision:
    def __init__(self, revision_id, document_id, author_id, timestamp, notes, change_history):
        self.revision_id = revision_id
        self.document_id = document_id
        self.author_id = author_id
        self.timestamp = timestamp
        self.notes = notes
        self.change_history = change_history
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
from datetime import datetime, timedelta
from persons.Author import Author

@pytest.fixture
def author():
    return Author(
        author_id=1,
        fullname="Error Tester",
        email="error@example.com",
        document_id=101,
        created_at=datetime.now() - timedelta(days=10)
    )
def test_update_email_valid(author):
    author.update_email("new@example.com")
    assert author.email == "new@example.com"

def test_update_email_invalid(author):
    author.update_email("invalid-email")
    assert author.email != "invalid-email"

def test_is_associated_with_true(author):
    assert author.is_associated_with(101) is True

def test_is_associated_with_false(author):
    assert author.is_associated_with(999) is False

def test_get_initials(author):
    assert author.get_initials() == "ET"

def test_is_recent_true(author):
    assert author.is_recent(days=30) is True

def test_is_recent_false(author):
    author.created_at = datetime.now() - timedelta(days=60)
    assert author.is_recent(days=30) is False

def test_format_for_display(author):
    output = author.format_for_display()
    assert f"Автор #{author.author_id}" in output
    assert author.fullname in output
    assert author.email in output

def test_to_dict(author):
    data = author.to_dict()
    assert data["author_id"] == 1
    assert data["fullname"] == "Error Tester"
    assert data["email"] == "error@example.com"
    assert data["document_id"] == 101
    assert isinstance(data["created_at"], str)

def test_is_author_of_true(author):
    doc = DummyDocument(document_id=101)
    assert author.is_author_of(doc) is True

def test_is_author_of_false(author):
    doc = DummyDocument(document_id=999)
    assert author.is_author_of(doc) is False

