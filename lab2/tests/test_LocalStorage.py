from datetime import datetime

class DummyBackup:
    def __init__(self, backup_id, size_mb=None, timestamp=None, location=None):
        self.backup_id = backup_id
        self.size_mb = size_mb
        self.timestamp = timestamp or datetime(2025, 1, 1)
        self.location = location

class DummyFolder:
    def __init__(self, folder_id, name, document_ids):
        self.folder_id = folder_id
        self.name = name
        self.document_ids = document_ids

class DummyDocument:
    def __init__(self, document_id, title):
        self.document_id = document_id
        self.title = title
import pytest
from storage_and_access.LocalStorage import LocalStorage

@pytest.fixture
def storage():
    return LocalStorage(path="/mnt/data", capacity_gb=500.0)
def test_update_path_valid(storage):
    storage.update_path("/new/path")
    assert storage.path == "/new/path"

def test_update_path_empty(storage):
    storage.update_path("")
    assert storage.path == "/mnt/data"  # не должен измениться

def test_resize_valid(storage):
    storage.resize(750.0)
    assert storage.capacity_gb == 750.0

def test_resize_invalid(storage):
    storage.resize(-100.0)
    assert storage.capacity_gb == 500.0  # не должен измениться

def test_is_path_valid_true(storage):
    assert storage.is_path_valid() is True

def test_is_path_valid_false():
    s = LocalStorage(path="C:\\storage", capacity_gb=100)
    assert s.is_path_valid() is False

def test_has_enough_space_true(storage):
    assert storage.has_enough_space(100.0) is True

def test_has_enough_space_false(storage):
    assert storage.has_enough_space(600.0) is False

def test_summarize_output(storage):
    summary = storage.summarize()
    assert "Локальное хранилище" in summary
    assert "/mnt/data" in summary
    assert "500.0 GB" in summary

def test_to_dict_format(storage):
    data = storage.to_dict()
    assert data == {"path": "/mnt/data", "capacity_gb": 500.0}

def test_store_backup_sets_location(storage):
    backup = DummyBackup(1)
    storage.store_backup(backup)
    assert backup.location == "/mnt/data"

def test_get_backup_summary(storage):
    backup = DummyBackup(2, size_mb=250.0)
    summary = storage.get_backup_summary(backup)
    assert "Резервная копия #2 размещена в '/mnt/data'" in summary
    assert "250.0 MB" in summary
    assert "2025-01-01" in summary

def test_store_folder_output(storage):
    folder = DummyFolder(10, "Исследования", [1, 2, 3])
    result = storage.store_folder(folder)
    assert "Папка 'Исследования' (#10)" in result
    assert "3 документами" in result

def test_store_documents_output(storage):
    docs = [DummyDocument(1, "A"), DummyDocument(2, "B")]
    result = storage.store_documents(docs)
    assert result == [
        "Документ 'A' (#1) сохранён в '/mnt/data'",
        "Документ 'B' (#2) сохранён в '/mnt/data'"
    ]

def test_export_storage_report(storage):
    backups = [
        DummyBackup(1, 100.0, datetime(2025, 1, 1), location="/mnt/data"),
        DummyBackup(2, 200.0, datetime(2025, 2, 1), location="/mnt/data"),
        DummyBackup(3, 300.0, datetime(2025, 3, 1), location="/other/path")
    ]
    report = storage.export_storage_report(backups)
    assert "Хранилище: /mnt/data | Объём: 500.0 GB" in report
    assert "— Backup #1 | 100.0 MB | 2025-01-01" in report
    assert "— Backup #2 | 200.0 MB | 2025-02-01" in report
    assert "Backup #3" not in report
