import pytest
from models.passenger.Passport import Passport

@pytest.fixture
def passport():
    return Passport("P123456", "Belarus", "2025-12-31")

def test_valid_passport(passport):
    assert passport.is_valid("2025-11-06") is True

def test_expired_passport(passport):
    assert passport.is_valid("2026-01-01") is False

def test_invalid_date_format(passport):
    assert passport.is_valid("06-11-2025") is False
    assert "Invalid date format: 06-11-2025" in passport.notes

def test_days_until_expiry(passport):
    assert passport.days_until_expiry("2025-11-06") == 55

def test_days_until_expiry_invalid(passport):
    assert passport.days_until_expiry("invalid-date") == 0

def test_assign_owner(passport):
    passport.assign_owner("Alice")
    assert passport.owner_name == "Alice"
    assert "Assigned to Alice" in passport.notes

def test_add_note(passport):
    passport.add_note("Damaged corner")
    assert "Damaged corner" in passport.notes

def test_summary_valid(passport):
    passport.assign_owner("Bob")
    summary = passport.summary()
    assert "Passport P123456 (Belarus)" in summary
    assert "Owner: Bob" in summary

def test_requires_renewal_notice_true(passport):
    assert passport.requires_renewal_notice("2025-11-06", threshold_days=60) is True

def test_requires_renewal_notice_false(passport):
    assert passport.requires_renewal_notice("2025-01-01", threshold_days=60) is False

def test_requires_renewal_notice_invalid(passport):
    assert passport.requires_renewal_notice("bad-date") is False
    assert "Invalid date format: bad-date" in passport.notes

def test_get_expiry_status_valid(passport):
    assert passport.get_expiry_status("2025-01-01") == "Valid"

def test_get_expiry_status_expiring_soon(passport):
    assert passport.get_expiry_status("2025-12-15", threshold_days=20) == "Expiring Soon"

def test_get_expiry_status_expired(passport):
    assert passport.get_expiry_status("2026-01-01") == "Expired"

def test_get_expiry_status_invalid(passport):
    assert passport.get_expiry_status("bad-date") == "Unknown"
    assert "Invalid date format: bad-date" in passport.notes

def test_flag_if_expired_true(passport):
    assert passport.flag_if_expired("2026-01-01") is True
    assert "Passport flagged as expired." in passport.notes

def test_flag_if_expired_false(passport):
    assert passport.flag_if_expired("2025-11-06") is False

def test_to_dict(passport):
    passport.assign_owner("Charlie")
    passport.add_note("Stamped in 2023")
    d = passport.to_dict()
    assert d["number"] == "P123456"
    assert d["nationality"] == "Belarus"
    assert d["expiration_date"] == "2025-12-31"
    assert d["owner_name"] == "Charlie"
    assert "Stamped in 2023" in d["notes"]
    assert d["notes"] is not passport.notes  # ensure it's a copy
