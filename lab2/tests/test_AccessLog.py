class DummyUserProfile:
    def __init__(self, expert_id, email):
        self.expert_id = expert_id
        self.email = email

class DummyDocument:
    def __init__(self, document_id):
        self.document_id = document_id
import pytest
from datetime import datetime, timedelta
from storage_and_access.AccessLog import AccessLog

@pytest.fixture
def access_log():
    return AccessLog(
        user_id=1,
        action="view",
        email="user@example.com",
        timestamp=datetime.now() - timedelta(minutes=30),
        document_id=101
    )
def test_action_valid(access_log):
    access_log.action = "edit"
    assert access_log.action == "edit"

def test_action_invalid(access_log):
    with pytest.raises(ValueError):
        access_log.action = "delete"

def test_is_for_document_true(access_log):
    assert access_log.is_for_document(101) is True

def test_is_for_document_false(access_log):
    assert access_log.is_for_document(999) is False

def test_is_recent_true(access_log):
    assert access_log.is_recent(minutes=60) is True

def test_is_recent_false(access_log):
    access_log.timestamp = datetime.now() - timedelta(hours=2)
    assert access_log.is_recent(minutes=60) is False

def test_is_action_true(access_log):
    access_log.action = "download"
    assert access_log.is_action("download") is True

def test_is_action_false(access_log):
    assert access_log.is_action("edit") is False

def test_summarize_output(access_log):
    summary = access_log.summarize()
    assert "Доступ: view" in summary
    assert "Пользователь ID: 1" in summary
    assert "Документ #101" in summary

def test_to_dict_format(access_log):
    data = access_log.to_dict()
    assert data["user_id"] == 1
    assert data["action"] == "view"
    assert isinstance(data["timestamp"], str)
    assert data["document_id"] == 101

def test_is_by_user_true(access_log):
    assert access_log.is_by_user(1) is True

def test_is_by_user_false(access_log):
    assert access_log.is_by_user(999) is False

def test_matches_user_profile_true(access_log):
    profile = DummyUserProfile(expert_id=1, email="user@example.com")
    assert access_log.matches_user_profile(profile) is True

def test_matches_user_profile_false(access_log):
    profile = DummyUserProfile(expert_id=2, email="other@example.com")
    assert access_log.matches_user_profile(profile) is False

def test_email_matches_true(access_log):
    assert access_log.email_matches("user@example.com") is True

def test_email_matches_false(access_log):
    assert access_log.email_matches("wrong@example.com") is False

def test_is_related_to_true(access_log):
    doc = DummyDocument(document_id=101)
    assert access_log.is_related_to(doc) is True

def test_is_related_to_false(access_log):
    doc = DummyDocument(document_id=999)
    assert access_log.is_related_to(doc) is False

def test_generate_audit_entry(access_log):
    entry = access_log.generate_audit_entry()
    assert entry["user_id"] == 1
    assert entry["action"] == "view"
    assert entry["document_id"] == 101
    assert isinstance(entry["timestamp"], str)

def test_format_for_notification(access_log):
    note = access_log.format_for_notification()
    assert "Пользователь #1" in note
    assert "действие 'view'" in note
    assert "документ #101" in note
