import pytest
from models.infrastructure.Gate import Gate
from exceptions.GateConflictException import GateConflictException

class DummyFlight:
    def __init__(self, flight_number):
        self.flight_number = flight_number

class DummyTerminal:
    def __init__(self, name):
        self.name = name

class DummyGroundStaff:
    def __init__(self, name, role):
        self.name = name
        self.role = role

@pytest.fixture
def gate():
    return Gate(gate_number="A1", terminal=DummyTerminal("T1"))

def test_assign_flight_success(gate):
    flight = DummyFlight("FL123")
    gate.assign_flight(flight)
    assert gate.current_flight == flight
    assert gate.history == ["FL123"]

def test_assign_flight_conflict(gate):
    flight1 = DummyFlight("FL123")
    flight2 = DummyFlight("FL999")
    gate.assign_flight(flight1)
    with pytest.raises(GateConflictException):
        gate.assign_flight(flight2)

def test_release_flight(gate):
    flight = DummyFlight("FL123")
    gate.assign_flight(flight)
    gate.release_flight()
    assert gate.current_flight is None

def test_is_available_true(gate):
    assert gate.is_available() is True

def test_is_available_false_due_to_flight(gate):
    gate.assign_flight(DummyFlight("FL123"))
    assert gate.is_available() is False

def test_is_available_false_due_to_maintenance(gate):
    gate.mark_for_maintenance()
    assert gate.is_available() is False

def test_is_available_false_due_to_shutdown(gate):
    gate.shutdown()
    assert gate.is_available() is False

def test_mark_and_clear_maintenance(gate):
    gate.mark_for_maintenance()
    assert gate.maintenance_required is True
    gate.clear_maintenance()
    assert gate.maintenance_required is False

def test_shutdown_and_restart(gate):
    gate.shutdown()
    assert gate.is_operational is False
    gate.restart()
    assert gate.is_operational is True

def test_assign_staff(gate):
    staff = DummyGroundStaff("Ivan", "Security")
    gate.assign_staff(staff)
    assert gate.assigned_staff == [staff]

def test_get_staff_by_role(gate):
    s1 = DummyGroundStaff("Anna", "Security")
    s2 = DummyGroundStaff("Leo", "Check-in")
    gate.assign_staff(s1)
    gate.assign_staff(s2)
    result = gate.get_staff_by_role("Security")
    assert result == [s1]

def test_has_flight_true(gate):
    flight = DummyFlight("FL123")
    gate.assign_flight(flight)
    assert gate.has_flight("FL123") is True

def test_has_flight_false(gate):
    assert gate.has_flight("UNKNOWN") is False

def test_get_terminal_name(gate):
    assert gate.get_terminal_name() == "T1"

def test_get_recent_flights_limit(gate):
    for i in range(10):
        gate.release_flight()  # освобождаем предыдущий рейс
        gate.assign_flight(DummyFlight(f"FL{i}"))
    recent = gate.get_recent_flights(limit=3)
    assert recent == ["FL7", "FL8", "FL9"]

