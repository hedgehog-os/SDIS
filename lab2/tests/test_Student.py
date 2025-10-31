class DummyUserProfile:
    def __init__(self, user_id, username, role, status):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.status = status
import pytest
from datetime import datetime, timedelta
from persons.Student import Student

@pytest.fixture
def student():
    return Student(
        student_id=1,
        fullname="Error Student",
        email="error@student.edu",
        department="Physics"
    )
def test_assign_document(student):
    student.assign_document(101)
    assert 101 in student.assigned_documents

def test_assign_document_duplicate(student):
    student.assign_document(101)
    student.assign_document(101)
    assert student.assigned_documents.count(101) == 1

def test_remove_document(student):
    student.assign_document(202)
    student.remove_document(202)
    assert 202 not in student.assigned_documents

def test_remove_document_missing(student):
    student.remove_document(999)  # не должно вызвать ошибку
    assert 999 not in student.assigned_documents

def test_has_document_true(student):
    student.assign_document(303)
    assert student.has_document(303) is True

def test_has_document_false(student):
    assert student.has_document(404) is False

def test_log_activity(student):
    student.log_activity("opened_document")
    assert "opened_document" in student.activity_log

def test_get_last_activity(student):
    student.log_activity("viewed")
    student.log_activity("edited")
    last = student.get_last_activity()
    assert last[0] == "edited"
    assert isinstance(last[1], datetime)

def test_get_last_activity_none(student):
    assert student.get_last_activity() is None

def test_get_recent_activities(student):
    now = datetime.now()
    student.activity_log = {
        "login": now - timedelta(minutes=10),
        "upload": now - timedelta(hours=2),
        "comment": now - timedelta(minutes=30)
    }
    recent = student.get_recent_activities(minutes=60)
    assert "login" in recent
    assert "comment" in recent
    assert "upload" not in recent

def test_update_profile(student):
    profile = DummyUserProfile(1, "error_user", "student", "active")
    student.update_profile(profile)
    assert student.profile == profile

def test_get_profile_summary_attached(student):
    profile = DummyUserProfile(2, "error_user", "student", "active")
    student.update_profile(profile)
    summary = student.get_profile_summary()
    assert "error_user" in summary
    assert "student" in summary
    assert "active" in summary

def test_get_profile_summary_unattached(student):
    assert student.get_profile_summary() == "Профиль не привязан."

def test_summarize_output(student):
    student.assign_document(101)
    student.log_activity("read")
    summary = student.summarize()
    assert f"Студент #{student.student_id}" in summary
    assert "Документов назначено: 1" in summary
    assert "Последняя активность: read" in summary

def test_to_dict_format(student):
    student.assign_document(101)
    student.log_activity("login")
    profile = DummyUserProfile(3, "error_user", "student", "active")
    student.update_profile(profile)
    data = student.to_dict()
    assert data["student_id"] == 1
    assert data["fullname"] == "Error Student"
    assert data["email"] == "error@student.edu"
    assert data["department"] == "Physics"
    assert data["assigned_documents"] == [101]
    assert "login" in data["activity_log"]
    assert isinstance(data["activity_log"]["login"], str)
    assert data["profile_id"] == 3
