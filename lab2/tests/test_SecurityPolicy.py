class DummyPermission:
    def __init__(self):
        self.can_view = True
        self.can_edit = True
        self.can_delete = True

class DummyDocument:
    def __init__(self):
        self.status = "final"
import pytest
from storage_and_access.SecurityPolicy import SecurityPolicy

@pytest.fixture
def policy():
    return SecurityPolicy(
        policy_id=1,
        name="Ограничения доступа",
        rules=["no_edit", "restricted_access"],
        enforced=True
    )
def test_add_rule(policy):
    policy.add_rule("no_delete")
    assert "no_delete" in policy.rules

def test_add_rule_duplicate(policy):
    initial_count = len(policy.rules)
    policy.add_rule("no_edit")
    assert len(policy.rules) == initial_count  # не должно добавиться повторно

def test_remove_rule(policy):
    policy.remove_rule("no_edit")
    assert "no_edit" not in policy.rules

def test_remove_rule_missing(policy):
    policy.remove_rule("nonexistent")
    assert "no_edit" in policy.rules  # ничего не должно измениться

def test_clear_rules(policy):
    policy.clear_rules()
    assert policy.rules == []

def test_is_rule_enforced_true(policy):
    assert policy.is_rule_enforced("no_edit") is True

def test_is_rule_enforced_false(policy):
    assert policy.is_rule_enforced("no_delete") is False

def test_applies_to_true(policy):
    assert policy.applies_to(["no_edit", "restricted_access"]) is True

def test_applies_to_false(policy):
    assert policy.applies_to(["no_edit", "no_delete"]) is False

def test_enable(policy):
    policy.disable()
    policy.enable()
    assert policy.enforced is True

def test_disable(policy):
    policy.disable()
    assert policy.enforced is False

def test_toggle(policy):
    original = policy.enforced
    policy.toggle()
    assert policy.enforced != original

def test_summarize_output(policy):
    summary = policy.summarize()
    assert "Политика #1" in summary
    assert "Активна" in summary
    assert "no_edit" in summary

def test_to_dict_format(policy):
    data = policy.to_dict()
    assert data["policy_id"] == 1
    assert data["name"] == "Ограничения доступа"
    assert data["rules"] == ["no_edit", "restricted_access"]
    assert data["enforced"] is True

def test_enforce_on_permission(policy):
    perm = DummyPermission()
    policy.enforce_on_permission(perm)
    assert perm.can_edit is False
    assert perm.can_delete is True  # no_delete не было в rules

def test_enforce_on_permission_with_no_delete():
    p = SecurityPolicy(2, "Полная блокировка", ["no_edit", "no_delete"], True)
    perm = DummyPermission()
    p.enforce_on_permission(perm)
    assert perm.can_edit is False
    assert perm.can_delete is False

def test_restrict_document_access(policy):
    doc = DummyDocument()
    policy.restrict_document_access(doc)
    assert doc.status == "restricted"

def test_restrict_document_access_not_enforced():
    p = SecurityPolicy(3, "Ограничение", ["restricted_access"], enforced=False)
    doc = DummyDocument()
    p.restrict_document_access(doc)
    assert doc.status == "final"
