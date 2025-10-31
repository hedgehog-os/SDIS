import pytest
from persons.ExternalExpert import ExternalExpert

@pytest.fixture
def expert():
    return ExternalExpert(
        expert_id=1,
        username="error_user",
        email="error@example.com",
        phone_number="1234567890",
        security_question="Ваш любимый цвет?",
        two_factor_enabled=False,
        preferred_language="ru",
        timezone="Europe/Minsk",
        account_status="active"
    )
def test_account_status_valid(expert):
    expert.account_status = "suspended"
    assert expert.account_status == "suspended"

def test_account_status_invalid(expert):
    with pytest.raises(ValueError):
        expert.account_status = "unknown"

def test_enable_two_factor(expert):
    expert.enable_two_factor()
    assert expert.two_factor_enabled is True

def test_disable_two_factor(expert):
    expert.enable_two_factor()
    expert.disable_two_factor()
    assert expert.two_factor_enabled is False

def test_update_email_valid(expert):
    expert.update_email("new@example.com")
    assert expert.email == "new@example.com"

def test_update_email_invalid(expert):
    expert.update_email("invalid-email")
    assert expert.email != "invalid-email"  # email не должен обновиться

def test_update_phone_valid(expert):
    expert.update_phone("9876543210")
    assert expert.phone_number == "9876543210"

def test_update_phone_invalid(expert):
    expert.update_phone("abc123")
    assert expert.phone_number != "abc123"

def test_reset_security_question(expert):
    expert.reset_security_question("Ваш первый питомец?")
    assert expert.security_question == "Ваш первый питомец?"

def test_set_language(expert):
    expert.set_language("en")
    assert expert.preferred_language == "en"

def test_set_timezone(expert):
    expert.set_timezone("UTC")
    assert expert.timezone == "UTC"

def test_is_active(expert):
    expert.account_status = "active"
    assert expert.is_active() is True

def test_is_pending(expert):
    expert.account_status = "pending"
    assert expert.is_pending() is True

def test_is_suspended(expert):
    expert.account_status = "suspended"
    assert expert.is_suspended() is True

def test_summarize_output(expert):
    summary = expert.summarize()
    assert f"Эксперт #{expert.expert_id}" in summary
    assert "2FA: отключена" in summary

def test_to_dict_contains_all_fields(expert):
    data = expert.to_dict()
    assert data["expert_id"] == 1
    assert data["username"] == "error_user"
    assert data["email"] == "error@example.com"
    assert data["phone_number"] == "1234567890"
    assert data["security_question"] == "Ваш любимый цвет?"
    assert data["two_factor_enabled"] is False
    assert data["preferred_language"] == "ru"
    assert data["timezone"] == "Europe/Minsk"
    assert data["account_status"] == "active"
