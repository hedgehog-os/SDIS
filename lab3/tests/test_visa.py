import pytest
from models.passenger.Visa import Visa

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

@pytest.fixture
def visa():
    return Visa("Germany", "Tourist", "2025-12-31")

def test_is_valid_true(visa):
    assert visa.is_valid("2025-11-06") is True

def test_is_valid_false(visa):
    assert visa.is_valid("2026-01-01") is False

def test_is_valid_invalid_format(visa):
    assert visa.is_valid("06-11-2025") is False
    assert "Invalid date format: 06-11-2025" in visa.notes

def test_assign_holder(visa):
    passenger = DummyPassenger("Alice")
    visa.assign_holder(passenger)
    assert visa.holder == passenger
    assert "Assigned to Alice" in visa.notes

def test_add_note(visa):
    visa.add_note("Stamped at border")
    assert "Stamped at border" in visa.notes

def test_get_expiry_status_valid(visa):
    assert visa.get_expiry_status("2025-01-01") == "Valid"

def test_get_expiry_status_expiring_soon(visa):
    assert visa.get_expiry_status("2025-12-15", threshold_days=20) == "Expiring Soon"

def test_get_expiry_status_expired(visa):
    assert visa.get_expiry_status("2026-01-01") == "Expired"

def test_get_expiry_status_invalid_format(visa):
    assert visa.get_expiry_status("bad-date") == "Unknown"

def test_to_dict(visa):
    passenger = DummyPassenger("Bob")
    visa.assign_holder(passenger)
    visa.add_note("Issued in 2023")
    d = visa.to_dict()
    assert d["country"] == "Germany"
    assert d["visa_type"] == "Tourist"
    assert d["expiration_date"] == "2025-12-31"
    assert d["holder_name"] == "Bob"
    assert "Issued in 2023" in d["notes"]
    assert d["notes"] is not visa.notes  # ensure it's a copy

def test_summary_unassigned(visa):
    summary = visa.summary()
    assert "Holder: Unassigned" in summary

def test_summary_assigned(visa):
    passenger = DummyPassenger("Charlie")
    visa.assign_holder(passenger)
    summary = visa.summary()
    assert "Holder: Charlie" in summary
