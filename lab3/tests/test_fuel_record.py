import pytest
from models.operations.fuel_record import FuelRecord

class DummyAircraft:
    def __init__(self, registration, max_fuel_capacity_liters):
        self.registration = registration
        self.max_fuel_capacity_liters = max_fuel_capacity_liters

def test_valid_initialization():
    aircraft = DummyAircraft("EW-001", 20000)
    record = FuelRecord(aircraft, 15000.0, "2025-11-06T10:00")
    assert record.aircraft == aircraft
    assert record.fuel_liters == 15000.0
    assert record.timestamp == "2025-11-06T10:00"
    assert record.is_verified is False
    assert record.notes == []

def test_negative_fuel_liters():
    aircraft = DummyAircraft("EW-002", 18000)
    with pytest.raises(ValueError, match="Fuel amount cannot be negative."):
        FuelRecord(aircraft, -100.0, "2025-11-06T10:00")

@pytest.fixture
def record():
    aircraft = DummyAircraft("EW-003", 25000)
    return FuelRecord(aircraft, 12000.0, "2025-11-06T12:00")

def test_verify(record):
    record.verify()
    assert record.is_verified is True

def test_invalidate(record):
    record.invalidate("Sensor mismatch")
    assert record.is_verified is False
    assert record.notes == ["Invalidated: Sensor mismatch"]

def test_add_note(record):
    record.add_note("Manual entry confirmed")
    assert record.notes == ["Manual entry confirmed"]

def test_reset(record):
    record.verify()
    record.add_note("Initial check")
    record.reset()
    assert record.is_verified is False
    assert record.notes == []

def test_summary_verified(record):
    record.verify()
    assert record.summary() == "FuelRecord for EW-003 at 2025-11-06T12:00: 12000.00 L, VERIFIED"

def test_summary_unverified(record):
    assert record.summary() == "FuelRecord for EW-003 at 2025-11-06T12:00: 12000.00 L, UNVERIFIED"

def test_is_excessive_false(record):
    assert record.is_excessive() is False

def test_is_excessive_true():
    aircraft = DummyAircraft("EW-004", 10000)
    record = FuelRecord(aircraft, 12000.0, "2025-11-06T13:00")
    assert record.is_excessive() is True

def test_fuel_percentage(record):
    expected = round((12000.0 / 25000.0) * 100, 2)
    assert record.fuel_percentage() == expected
