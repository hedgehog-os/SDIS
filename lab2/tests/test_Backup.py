class DummyEncryption:
    def __init__(self, method):
        self.method = method

class DummyStorageDevice:
    def __init__(self, name):
        self.name = name
import pytest
from datetime import datetime, timedelta
from storage_and_access.Backup import Backup

@pytest.fixture
def backup():
    return Backup(
        backup_id=1,
        location="Shelf A",
        timestamp=datetime.now() - timedelta(days=5),
        size_mb=120.0
    )
def test_encrypt_sets_method(backup):
    method = DummyEncryption("AES-256")
    backup.encrypt(method)
    assert backup.encrypted_with == method
    assert backup.is_encrypted() is True

def test_decrypt_clears_encryption(backup):
    method = DummyEncryption("RSA")
    backup.encrypt(method)
    backup.decrypt()
    assert backup.encrypted_with is None
    assert backup.is_encrypted() is False

def test_assign_to_device_sets_device(backup):
    device = DummyStorageDevice("Disk 1")
    backup.assign_to_device(device)
    assert backup.storage_device == device

def test_is_stored_on_true(backup):
    device = DummyStorageDevice("Disk 2")
    backup.assign_to_device(device)
    assert backup.is_stored_on(device) is True

def test_is_stored_on_false(backup):
    device1 = DummyStorageDevice("Disk A")
    device2 = DummyStorageDevice("Disk B")
    backup.assign_to_device(device1)
    assert backup.is_stored_on(device2) is False

def test_is_recent_true(backup):
    assert backup.is_recent(days=10) is True

def test_is_recent_false(backup):
    old_backup = Backup(2, "Shelf B", timestamp=datetime.now() - timedelta(days=60))
    assert old_backup.is_recent(days=30) is False

def test_is_large_true(backup):
    assert backup.is_large(threshold_mb=100.0) is True

def test_is_large_false(backup):
    small_backup = Backup(3, "Shelf C", size_mb=50.0)
    assert small_backup.is_large(threshold_mb=100.0) is False

def test_summarize_output(backup):
    method = DummyEncryption("AES")
    device = DummyStorageDevice("Disk X")
    backup.encrypt(method)
    backup.assign_to_device(device)
    summary = backup.summarize()
    assert f"Резервная копия #{backup.backup_id}" in summary
    assert "Шифрование: AES" in summary
    assert "Устройство: Disk X" in summary

def test_to_dict_format(backup):
    method = DummyEncryption("AES")
    device = DummyStorageDevice("Disk Y")
    backup.encrypt(method)
    backup.assign_to_device(device)
    data = backup.to_dict()
    assert data["backup_id"] == 1
    assert data["location"] == "Shelf A"
    assert isinstance(data["timestamp"], str)
    assert data["size_mb"] == 120.0
    assert data["encrypted_with"] == "AES"
    assert data["storage_device"] == "Disk Y"
