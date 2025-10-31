from datetime import datetime

class DummyDocument:
    def __init__(self, document_id, title, status):
        self.document_id = document_id
        self.title = title
        self.status = status

class DummyArchive:
    def __init__(self):
        self.documents = []

class DummyReport:
    def __init__(self, author_id, title):
        self.author_id = author_id
        self.title = title
        self.comments = []

class DummyComment:
    def __init__(self, comment_id, document_id, user_id, content, posted_at):
        self.comment_id = comment_id
        self.document_id = document_id
        self.user_id = user_id
        self.content = content
        self.posted_at = posted_at
import pytest
from storage_and_access.Folder import Folder

@pytest.fixture
def folder():
    return Folder(
        folder_id=1,
        name="Исследования",
        parent_id=None,
        document_ids=[101, 102, 103]
    )
def test_add_document(folder):
    folder.add_document(104)
    assert 104 in folder.document_ids

def test_add_document_duplicate(folder):
    folder.add_document(101)
    assert folder.document_ids.count(101) == 1

def test_remove_document(folder):
    folder.remove_document(102)
    assert 102 not in folder.document_ids

def test_remove_document_missing(folder):
    folder.remove_document(999)  # не должно вызвать ошибку
    assert 999 not in folder.document_ids

def test_has_document_true(folder):
    assert folder.has_document(103) is True

def test_has_document_false(folder):
    assert folder.has_document(999) is False

def test_is_root_true(folder):
    assert folder.is_root() is True

def test_is_child_of_true():
    parent = Folder(10, "Родитель", None, [])
    child = Folder(11, "Дочерняя", parent_id=10, document_ids=[])
    assert child.is_child_of(parent) is True

def test_count_documents(folder):
    assert folder.count_documents() == 3

def test_get_documents_by_prefix(folder):
    folder.document_ids.append(201)
    result = folder.get_documents_by_prefix("10")
    assert set(result) == {101, 102, 103}

def test_summarize_output(folder):
    summary = folder.summarize()
    assert "Папка #1" in summary
    assert "Корневая папка" in summary
    assert "Документов: 3" in summary

def test_to_dict_format(folder):
    data = folder.to_dict()
    assert data["folder_id"] == 1
    assert data["name"] == "Исследования"
    assert data["parent_id"] is None
    assert data["document_ids"] == [101, 102, 103]

def test_get_documents(folder):
    docs = [DummyDocument(101, "A", "draft"), DummyDocument(999, "X", "final")]
    result = folder.get_documents(docs)
    assert len(result) == 1
    assert result[0].document_id == 101

def test_get_documents_by_status(folder):
    docs = [
        DummyDocument(101, "A", "draft"),
        DummyDocument(102, "B", "final"),
        DummyDocument(103, "C", "draft")
    ]
    result = folder.get_documents_by_status(docs, "draft")
    assert len(result) == 2

def test_get_document_titles(folder):
    docs = [
        DummyDocument(101, "A", "draft"),
        DummyDocument(102, "B", "final"),
        DummyDocument(103, "C", "archived")
    ]
    titles = folder.get_document_titles(docs)
    assert titles == ["A", "B", "C"]

def test_archive_contents(folder):
    archive = DummyArchive()
    folder.archive_contents(archive)
    assert set(archive.documents) == {101, 102, 103}

def test_export_summary(folder):
    docs = [
        DummyDocument(101, "A", "draft"),
        DummyDocument(102, "B", "final"),
        DummyDocument(103, "C", "archived")
    ]
    summary = folder.export_summary(docs)
    assert "Папка #1" in summary
    assert "— A [draft]" in summary
    assert "— C [archived]" in summary
