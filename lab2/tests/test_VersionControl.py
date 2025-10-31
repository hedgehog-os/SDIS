import pytest
from storage_and_access.VersionControl import VersionControl

@pytest.fixture
def version_control():
    return VersionControl(
        document_id=101,
        versions=["v1.0", "v1.1", "v2.0"],
        current_version="v2.0"
    )
def test_add_version_new(version_control):
    version_control.add_version("v2.1")
    assert "v2.1" in version_control.versions
    assert version_control.current_version == "v2.1"

def test_add_version_existing(version_control):
    version_control.add_version("v1.1")
    assert version_control.current_version == "v1.1"
    assert version_control.versions.count("v1.1") == 1

def test_rollback_to_existing(version_control):
    result = version_control.rollback_to("v1.0")
    assert result is True
    assert version_control.current_version == "v1.0"

def test_rollback_to_nonexistent(version_control):
    result = version_control.rollback_to("v3.0")
    assert result is False
    assert version_control.current_version == "v2.0"

def test_remove_version_success(version_control):
    result = version_control.remove_version("v1.1")
    assert result is True
    assert "v1.1" not in version_control.versions

def test_remove_version_current(version_control):
    result = version_control.remove_version("v2.0")
    assert result is False
    assert "v2.0" in version_control.versions

def test_remove_version_nonexistent(version_control):
    result = version_control.remove_version("v3.0")
    assert result is False

def test_is_latest_true(version_control):
    assert version_control.is_latest("v2.0") is True

def test_is_latest_false(version_control):
    assert version_control.is_latest("v1.0") is False

def test_has_version_true(version_control):
    assert version_control.has_version("v1.1") is True

def test_has_version_false(version_control):
    assert version_control.has_version("v3.0") is False

def test_version_count(version_control):
    assert version_control.version_count() == 3

def test_summarize_output(version_control):
    summary = version_control.summarize()
    assert "Контроль версий для документа #101" in summary
    assert "Текущая версия: v2.0" in summary
    assert "Всего версий: 3" in summary
    assert "v1.0, v1.1, v2.0" in summary

def test_to_dict_format(version_control):
    data = version_control.to_dict()
    assert data["document_id"] == 101
    assert data["versions"] == ["v1.0", "v1.1", "v2.0"]
    assert data["current_version"] == "v2.0"
