class DummyBackup:
    def __init__(self, backup_id):
        self.backup_id = backup_id
        self.location = None
import pytest
from storage_and_access.CloudStorage import CloudStorage

@pytest.fixture
def cloud():
    return CloudStorage(
        provider="AWS",
        bucket_name="lab-data",
        access_key="abc123"
    )
def test_update_access_key(cloud):
    cloud.update_access_key("newkey456")
    assert cloud.access_key == "newkey456"

def test_update_access_key_empty(cloud):
    cloud.update_access_key("")
    assert cloud.access_key == "abc123"  # не должен измениться

def test_rename_bucket(cloud):
    cloud.rename_bucket("new-bucket")
    assert cloud.bucket_name == "new-bucket"

def test_rename_bucket_empty(cloud):
    cloud.rename_bucket("")
    assert cloud.bucket_name == "lab-data"  # не должен измениться

def test_is_valid_key_true(cloud):
    assert cloud.is_valid_key("abc123") is True

def test_is_valid_key_false(cloud):
    assert cloud.is_valid_key("wrongkey") is False

def test_belongs_to_provider_true(cloud):
    assert cloud.belongs_to_provider("aws") is True

def test_belongs_to_provider_false(cloud):
    assert cloud.belongs_to_provider("azure") is False

def test_summarize_output(cloud):
    summary = cloud.summarize()
    assert "Облако: AWS" in summary
    assert "Бакет: lab-data" in summary
    assert "*** скрыт ***" in summary

def test_to_dict_format(cloud):
    data = cloud.to_dict()
    assert data["provider"] == "AWS"
    assert data["bucket_name"] == "lab-data"
    assert data["access_key"] == "abc123"

def test_link_backup_sets_location(cloud):
    backup = DummyBackup(42)
    cloud.link_backup(backup)
    assert backup.location == "AWS/lab-data/backup_42"

def test_upload_file_simulation(cloud):
    result = cloud.upload_file("report.pdf", 12.5)
    assert "report.pdf" in result
    assert "12.5 MB" in result
    assert "lab-data" in result

def test_download_file_simulation(cloud):
    result = cloud.download_file("data.csv")
    assert "data.csv" in result
    assert "lab-data" in result

def test_check_quota_exceeded(cloud):
    msg = cloud.check_quota(150.0, 100.0)
    assert "Превышена квота" in msg

def test_check_quota_within_limit(cloud):
    msg = cloud.check_quota(80.0, 100.0)
    assert "в пределах лимита" in msg

def test_is_bucket_active_true(cloud):
    assert cloud.is_bucket_active() is True

def test_is_bucket_active_false():
    cloud = CloudStorage("AWS", "lab-data", "")
    assert cloud.is_bucket_active() is False

def test_generate_monitoring_entry(cloud):
    entry = cloud.generate_monitoring_entry("upload", "file.txt")
    assert entry["action"] == "upload"
    assert entry["file"] == "file.txt"
    assert entry["provider"] == "AWS"
    assert entry["bucket"] == "lab-data"
    assert entry["status"] == "success"
    assert "timestamp" in entry
