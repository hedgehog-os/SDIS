class DummyBackup:
    def __init__(self, backup_id):
        self.backup_id = backup_id
        self.encrypted_with = None
import pytest
from storage_and_access.Encryption import Encryption

@pytest.fixture
def encryption():
    return Encryption(
        encryption_id=1,
        method="AES",
        key_length=256,
        algorithm="GCM"
    )
def test_valid_method_and_algorithm(encryption):
    encryption.method = "RSA"
    encryption.algorithm = "CBC"
    assert encryption.method == "RSA"
    assert encryption.algorithm == "CBC"

def test_invalid_method(encryption):
    with pytest.raises(ValueError):
        encryption.method = "Blowfish"

def test_invalid_algorithm(encryption):
    with pytest.raises(ValueError):
        encryption.algorithm = "XYZ"

def test_apply_to_backup(encryption):
    backup = DummyBackup(42)
    encryption.apply_to_backup(backup)
    assert backup in encryption.applied_to
    assert backup.encrypted_with == encryption

def test_apply_to_backup_duplicate(encryption):
    backup = DummyBackup(42)
    encryption.apply_to_backup(backup)
    encryption.apply_to_backup(backup)
    assert encryption.applied_to.count(backup) == 1

def test_remove_from_backup(encryption):
    backup = DummyBackup(99)
    encryption.apply_to_backup(backup)
    encryption.remove_from_backup(backup)
    assert backup not in encryption.applied_to
    assert backup.encrypted_with is None

def test_remove_from_backup_not_applied(encryption):
    backup = DummyBackup(77)
    encryption.remove_from_backup(backup)  # не должно вызвать ошибку
    assert backup.encrypted_with is None

def test_is_strong_encryption_true(encryption):
    assert encryption.is_strong_encryption() is True

def test_is_strong_encryption_false():
    weak = Encryption(2, "AES", 128, "CBC")
    assert weak.is_strong_encryption() is False

def test_is_applied_to_true(encryption):
    backup = DummyBackup(55)
    encryption.apply_to_backup(backup)
    assert encryption.is_applied_to(backup) is True

def test_is_applied_to_false(encryption):
    backup = DummyBackup(56)
    assert encryption.is_applied_to(backup) is False

def test_summarize_output(encryption):
    backup = DummyBackup(1)
    encryption.apply_to_backup(backup)
    summary = encryption.summarize()
    assert f"Шифрование #{encryption.encryption_id}" in summary
    assert "Метод: AES" in summary
    assert "Алгоритм: GCM" in summary
    assert "Применено к 1 резервным копиям" in summary

def test_to_dict_format(encryption):
    backup1 = DummyBackup(10)
    backup2 = DummyBackup(20)
    encryption.apply_to_backup(backup1)
    encryption.apply_to_backup(backup2)
    data = encryption.to_dict()
    assert data["encryption_id"] == 1
    assert data["method"] == "AES"
    assert data["key_length"] == 256
    assert data["algorithm"] == "GCM"
    assert data["applied_to"] == [10, 20]
