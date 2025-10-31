class DummyUserProfile:
    def __init__(self, expert_id, username):
        self.expert_id = expert_id
        self.username = username

class DummyDocument:
    def __init__(self, document_id, title):
        self.document_id = document_id
        self.title = title

class DummyAccessLog:
    def __init__(self, user_id, document_id, action):
        self.user_id = user_id
        self.document_id = document_id
        self.action = action
import pytest
from storage_and_access.Permission import Permission

@pytest.fixture
def permission():
    return Permission(user_id=1, document_id=101, can_view=True, can_edit=False, can_delete=False)
def test_has_view_permission(permission):
    assert permission.has_view_permission() is True

def test_has_edit_permission(permission):
    assert permission.has_edit_permission() is False

def test_has_delete_permission(permission):
    assert permission.has_delete_permission() is False

def test_has_any_permission_true(permission):
    assert permission.has_any_permission() is True

def test_has_any_permission_false():
    p = Permission(1, 101, False, False, False)
    assert p.has_any_permission() is False

def test_grant_all(permission):
    permission.grant_all()
    assert permission.can_view and permission.can_edit and permission.can_delete

def test_revoke_all(permission):
    permission.revoke_all()
    assert not permission.can_view and not permission.can_edit and not permission.can_delete

def test_update_permissions(permission):
    permission.update_permissions(view=False, edit=True, delete=True)
    assert not permission.can_view
    assert permission.can_edit
    assert permission.can_delete

def test_summarize_output(permission):
    summary = permission.summarize()
    assert "Права пользователя #1" in summary
    assert "Просмотр: Разрешен" in summary
    assert "Редактирование: Запрещен" in summary

def test_to_dict_format(permission):
    data = permission.to_dict()
    assert data == {
        "user_id": 1,
        "document_id": 101,
        "can_view": True,
        "can_edit": False,
        "can_delete": False
    }

def test_applies_to_user_true(permission):
    user = DummyUserProfile(1, "Error")
    assert permission.applies_to_user(user) is True

def test_applies_to_user_false(permission):
    user = DummyUserProfile(2, "Other")
    assert permission.applies_to_user(user) is False

def test_applies_to_document_true(permission):
    doc = DummyDocument(101, "Документ")
    assert permission.applies_to_document(doc) is True

def test_applies_to_document_false(permission):
    doc = DummyDocument(999, "Другой")
    assert permission.applies_to_document(doc) is False

def test_enforce_on_document(permission):
    doc = DummyDocument(101, "Отчёт")
    result = permission.enforce_on_document(doc)
    assert "Пользователь может: просмотр" in result

def test_validate_access_log_allowed(permission):
    log = DummyAccessLog(1, 101, "view")
    assert permission.validate_access_log(log) is True

def test_validate_access_log_wrong_user(permission):
    log = DummyAccessLog(2, 101, "view")
    assert permission.validate_access_log(log) is False

def test_validate_access_log_wrong_document(permission):
    log = DummyAccessLog(1, 999, "view")
    assert permission.validate_access_log(log) is False

def test_validate_access_log_disallowed_action(permission):
    log = DummyAccessLog(1, 101, "delete")
    assert permission.validate_access_log(log) is False

def test_export_permission_report(permission):
    user = DummyUserProfile(1, "Error")
    doc = DummyDocument(101, "Файл")
    report = permission.export_permission_report(user, doc)
    assert "Пользователь: Error (#1)" in report
    assert "Документ: Файл (#101)" in report
    assert "Права: Просмотр — —" in report
