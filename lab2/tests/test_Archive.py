from datetime import datetime

class DummyDocument:
    def __init__(self, document_id, title, status):
        self.document_id = document_id
        self.title = title
        self.status = status
        self.restored = False

    def restore(self):
        self.status = "final"
        self.restored = True

class DummyBackup:
    def __init__(self, backup_id, timestamp, size_mb, storage_device):
        self.backup_id = backup_id
        self.timestamp = timestamp
        self.size_mb = size_mb
        self.storage_device = storage_device

class DummyStorageDevice:
    def __init__(self, name, location=None):
        self.name = name
        self.location = location
        self.backups = []

    def add_backup(self, backup):
        self.backups.append(backup)

class DummyReport:
    def __init__(self, report_id, title, author_id):
        self.report_id = report_id
        self.title = title
        self.author_id = author_id
        self.comments = []

class DummyComment:
    def __init__(self, comment_id, document_id, user_id, content, posted_at):
        self.comment_id = comment_id
        self.document_id = document_id
        self.user_id = user_id
        self.content = content
        self.posted_at = posted_at

class DummyForm:
    def __init__(self, form_id):
        self.form_id = form_id
import pytest
from datetime import datetime, timedelta
from storage_and_access.Archive import Archive
from Exceptions import ArchiveAlreadyContainsDocumentError, ArchiveDocumentNotFoundError

@pytest.fixture
def archive():
    return Archive(
        archive_id=1,
        name="Архив экспериментов",
        documents=[101, 102, 103],
        archived_at=datetime.now() - timedelta(days=10)
    )
def test_add_document_success(archive):
    archive.add_document(104)
    assert 104 in archive.documents

def test_add_document_duplicate(archive):
    with pytest.raises(ArchiveAlreadyContainsDocumentError):
        archive.add_document(101)

def test_remove_document_success(archive):
    archive.remove_document(102)
    assert 102 not in archive.documents

def test_remove_document_missing(archive):
    with pytest.raises(ArchiveDocumentNotFoundError):
        archive.remove_document(999)

def test_has_document_true(archive):
    assert archive.has_document(103) is True

def test_has_document_false(archive):
    assert archive.has_document(999) is False

def test_count_documents(archive):
    assert archive.count_documents() == 3

def test_get_documents_by_prefix(archive):
    archive.documents.append(201)
    result = archive.get_documents_by_prefix("10")
    assert set(result) == {101, 102, 103}

def test_summarize_output(archive):
    summary = archive.summarize()
    assert "Архив #1" in summary
    assert "Документов: 3" in summary

def test_to_dict_format(archive):
    data = archive.to_dict()
    assert data["archive_id"] == 1
    assert data["name"] == "Архив экспериментов"
    assert data["documents"] == [101, 102, 103]
    assert isinstance(data["archived_at"], str)

def test_get_documents(archive):
    docs = [DummyDocument(101, "Doc A", "draft"), DummyDocument(999, "Other", "final")]
    result = archive.get_documents(docs)
    assert len(result) == 1
    assert result[0].document_id == 101

def test_get_documents_by_status(archive):
    docs = [
        DummyDocument(101, "Doc A", "draft"),
        DummyDocument(102, "Doc B", "final"),
        DummyDocument(103, "Doc C", "draft")
    ]
    result = archive.get_documents_by_status(docs, "draft")
    assert len(result) == 2

def test_get_document_titles(archive):
    docs = [
        DummyDocument(101, "Doc A", "draft"),
        DummyDocument(102, "Doc B", "final"),
        DummyDocument(103, "Doc C", "archived")
    ]
    titles = archive.get_document_titles(docs)
    assert titles == ["Doc A", "Doc B", "Doc C"]

def test_export_summary(archive):
    docs = [
        DummyDocument(101, "Doc A", "draft"),
        DummyDocument(102, "Doc B", "final"),
        DummyDocument(103, "Doc C", "archived")
    ]
    summary = archive.export_summary(docs)
    assert "Архив #1" in summary
    assert "— Doc A [draft]" in summary

def test_restore_all_documents(archive):
    docs = [
        DummyDocument(101, "Doc A", "archived"),
        DummyDocument(102, "Doc B", "final"),
        DummyDocument(103, "Doc C", "archived")
    ]
    archive.restore_all_documents(docs)
    assert docs[0].status == "final"
    assert docs[2].status == "final"

def test_link_to_backup_true(archive):
    device = DummyStorageDevice(name="Disk A")
    device.backups = [101, 102, 103]
    backup = DummyBackup(1, datetime.now(), 10, device)
    assert archive.link_to_backup(backup) is True

def test_link_to_backup_false(archive):
    device = DummyStorageDevice(name="Disk A")
    device.backups = [101, 999]
    backup = DummyBackup(1, datetime.now(), 10, device)
    assert archive.link_to_backup(backup) is False

def test_generate_backup_summary(archive):
    device = DummyStorageDevice(name="Disk A")
    backup = DummyBackup(2, datetime(2025, 1, 1), 5, device)
    summary = archive.generate_backup_summary(backup)
    assert "Архив 'Архив экспериментов'" in summary
    assert "резервной копией #2" in summary


def test_validate_forms(archive):
    forms = [DummyForm(101), DummyForm(999), DummyForm(103)]
    result = archive.validate_forms(forms)
    assert [f.form_id for f in result] == [101, 103]
