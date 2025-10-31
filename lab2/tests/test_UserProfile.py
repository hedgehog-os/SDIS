import pytest
from datetime import datetime, timedelta

from Exceptions import PhoneNumberFormatError, EmailFormatError, SecurityQuestionEmptyError


from persons.UserProfile import UserProfile

@pytest.fixture
def profile():
    return UserProfile(
        expert_id=1,
        username="error_user",
        email="error@example.com",
        phone_number="1234567890",
        security_question="Ваш любимый цвет?",
        two_factor_enabled=False,
        preferred_language="ru",
        timezone="Europe/Minsk",
        account_status="active",
        registered_at=datetime.now() - timedelta(days=1)
    )


def test_account_status_valid(profile):
    profile.account_status = "suspended"
    assert profile.account_status == "suspended"

def test_account_status_invalid(profile):
    with pytest.raises(ValueError):
        profile.account_status = "unknown"

def test_enable_two_factor(profile):
    profile.enable_two_factor()
    assert profile.two_factor_enabled is True

def test_disable_two_factor(profile):
    profile.enable_two_factor()
    profile.disable_two_factor()
    assert profile.two_factor_enabled is False

def test_reset_security_question_valid(profile):
    profile.reset_security_question("Ваш первый питомец?")
    assert profile.security_question == "Ваш первый питомец?"

def test_reset_security_question_empty(profile):
    with pytest.raises(SecurityQuestionEmptyError):
        profile.reset_security_question("")

def test_update_email_valid(profile):
    profile.update_email("new@example.com")
    assert profile.email == "new@example.com"

def test_update_email_invalid(profile):
    with pytest.raises(EmailFormatError):
        profile.update_email("invalid-email")

def test_update_phone_valid(profile):
    profile.update_phone("9876543210")
    assert profile.phone_number == "9876543210"

def test_update_phone_invalid(profile):
    with pytest.raises(PhoneNumberFormatError):
        profile.update_phone("abc123")

def test_set_language(profile):
    profile.set_language("en")
    assert profile.preferred_language == "en"

def test_set_timezone(profile):
    profile.set_timezone("UTC")
    assert profile.timezone == "UTC"

def test_is_active(profile):
    profile.account_status = "active"
    assert profile.is_active() is True

def test_is_suspended(profile):
    profile.account_status = "suspended"
    assert profile.is_suspended() is True

def test_is_pending(profile):
    profile.account_status = "pending"
    assert profile.is_pending() is True

def test_summarize_output(profile):
    summary = profile.summarize()
    assert f"Профиль #{profile.expert_id}" in summary
    assert "2FA: отключена" in summary
    assert "Зарегистрирован: " in summary

def test_to_dict_format(profile):
    data = profile.to_dict()
    assert data["expert_id"] == 1
    assert data["username"] == "error_user"
    assert data["email"] == "error@example.com"
    assert data["phone_number"] == "1234567890"
    assert data["security_question"] == "Ваш любимый цвет?"
    assert data["two_factor_enabled"] is False
    assert data["preferred_language"] == "ru"
    assert data["timezone"] == "Europe/Minsk"
    assert data["account_status"] == "active"
    assert isinstance(data["registered_at"], str)
