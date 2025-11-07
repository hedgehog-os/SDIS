import pytest
from models.operations.maintenance_log import MaintenanceLog

class DummyAircraft:
    def __init__(self, registration):
        self.registration = registration

class DummyTechnician:
    def __init__(self, full_name):
        self.full_name = full_name

def test_valid_initialization():
    aircraft = DummyAircraft("EW-001")
    tech = DummyTechnician("Ivan Petrov")
    log = MaintenanceLog(aircraft, tech, "Engine vibration detected", "2025-11-06T10:00")
    assert log.aircraft == aircraft
    assert log.technician == tech
    assert log.notes == "Engine vibration detected"
    assert log.timestamp == "2025-11-06T10:00"
    assert log.is_resolved is False
    assert log.resolution_notes == []
    assert log.resolved_by is None

def test_empty_notes():
    aircraft = DummyAircraft("EW-002")
    tech = DummyTechnician("Olga Ivanova")
    with pytest.raises(ValueError, match="Maintenance notes cannot be empty."):
        MaintenanceLog(aircraft, tech, "   ", "2025-11-06T11:00")

@pytest.fixture
def log():
    aircraft = DummyAircraft("EW-003")
    tech = DummyTechnician("Sergey Volkov")
    return MaintenanceLog(aircraft, tech, "Hydraulic leak", "2025-11-06T12:00")

def test_mark_resolved(log):
    log.mark_resolved("Nikolai", "Leak sealed")
    assert log.is_resolved is True
    assert log.resolved_by == "Nikolai"
    assert log.resolution_notes == ["Leak sealed"]

def test_reopen(log):
    log.mark_resolved("Nikolai", "Initial fix")
    log.reopen("Leak reappeared")
    assert log.is_resolved is False
    assert log.resolved_by is None
    assert log.resolution_notes == ["Initial fix", "Leak reappeared"]

def test_add_resolution_note(log):
    log.add_resolution_note("Part replaced")
    assert log.resolution_notes == ["Part replaced"]

def test_reset(log):
    log.mark_resolved("Tech", "Fixed")
    log.add_resolution_note("Final check passed")
    log.reset()
    assert log.is_resolved is False
    assert log.resolved_by is None
    assert log.resolution_notes == []

def test_summary_open(log):
    summary = log.summary()
    assert summary == "MaintenanceLog for EW-003 at 2025-11-06T12:00 — OPEN, Technician: Sergey Volkov"

def test_summary_resolved(log):
    log.mark_resolved("Tech", "Resolved")
    summary = log.summary()
    assert summary == "MaintenanceLog for EW-003 at 2025-11-06T12:00 — RESOLVED by Tech, Technician: Sergey Volkov"
