from datetime import datetime, timedelta
from typing import Optional

class DummyBackup:
    def __init__(self, backup_id: int, size_mb: float = 0.0, timestamp: Optional[datetime] = None, encrypted_with: Optional[str] = None):
        self.backup_id = backup_id
        self.size_mb = size_mb
        self.timestamp = timestamp or datetime.now()
        self.encrypted_with = encrypted_with
        self.storage_device = None
import pytest
from experiments_and_equipments.StorageDevice import StorageDevice

@pytest.fixture
def storage():
    return StorageDevice(
        device_id=1,
        name="MainDisk",
        device_type="SSD",
        capacity_mb=1000.0,
        location="Lab A"
    )
def test_initial_state(storage):
    assert storage.device_id == 1
    assert storage.name == "MainDisk"
    assert storage.device_type == "SSD"
    assert storage.capacity_mb == 1000.0
    assert storage.location == "Lab A"
    assert storage.backups == []

def test_invalid_device_type():
    with pytest.raises(ValueError):
        StorageDevice(2, "BadDisk", "Tape", 500.0)

def test_add_backup(storage):
    b = DummyBackup(101, size_mb=100.0)
    storage.add_backup(b)
    assert b in storage.backups
    assert b.storage_device == storage

def test_add_backup_no_duplicate(storage):
    b = DummyBackup(102, size_mb=50.0)
    storage.add_backup(b)
    storage.add_backup(b)
    assert storage.backups.count(b) == 1

def test_remove_backup(storage):
    b = DummyBackup(103, size_mb=200.0)
    storage.add_backup(b)
    storage.remove_backup(b)
    assert b not in storage.backups
    assert b.storage_device is None

def test_total_backup_size(storage):
    b1 = DummyBackup(201, size_mb=300.0)
    b2 = DummyBackup(202, size_mb=150.0)
    storage.backups = [b1, b2]
    assert storage.total_backup_size() == 450.0

def test_available_space(storage):
    b1 = DummyBackup(301, size_mb=400.0)
    b2 = DummyBackup(302, size_mb=100.0)
    storage.backups = [b1, b2]
    assert storage.available_space() == 500.0

def test_is_over_capacity_true(storage):
    b1 = DummyBackup(401, size_mb=600.0)
    b2 = DummyBackup(402, size_mb=500.0)
    storage.backups = [b1, b2]
    assert storage.is_over_capacity() is True

def test_is_over_capacity_false(storage):
    b1 = DummyBackup(403, size_mb=200.0)
    b2 = DummyBackup(404, size_mb=300.0)
    storage.backups = [b1, b2]
    assert storage.is_over_capacity() is False

def test_get_recent_backups(storage):
    recent = DummyBackup(501, timestamp=datetime.now())
    old = DummyBackup(502, timestamp=datetime.now() - timedelta(days=60))
    storage.backups = [recent, old]
    result = storage.get_recent_backups(days=30)
    assert recent in result
    assert old not in result

def test_get_encrypted_backups(storage):
    b1 = DummyBackup(601, encrypted_with="AES")
    b2 = DummyBackup(602, encrypted_with=None)
    storage.backups = [b1, b2]
    result = storage.get_encrypted_backups()
    assert result == [b1]

def test_summarize(storage):
    b1 = DummyBackup(701, size_mb=100.0, encrypted_with="RSA")
    b2 = DummyBackup(702, size_mb=200.0)
    storage.backups = [b1, b2]
    summary = storage.summarize()
    assert "Устройство #1: MainDisk (SSD)" in summary
    assert "Расположение: Lab A" in summary
    assert "Ёмкость: 1000.00 MB" in summary
    assert "Использовано: 300.00 MB" in summary
    assert "Свободно: 700.00 MB" in summary
    assert "Резервных копий: 2 (1)" in summary

def test_to_dict(storage):
    b1 = DummyBackup(801, size_mb=100.0)
    b2 = DummyBackup(802, size_mb=200.0)
    storage.backups = [b1, b2]
    data = storage.to_dict()
    assert data["device_id"] == 1
    assert data["name"] == "MainDisk"
    assert data["device_type"] == "SSD"
    assert data["capacity_mb"] == 1000.0
    assert data["location"] == "Lab A"
    assert data["backup_ids"] == [801, 802]
    assert data["used_space_mb"] == 300.0
    assert data["free_space_mb"] == 700.0
