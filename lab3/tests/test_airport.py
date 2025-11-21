import pytest
from models.infrastructure.Airport import Airport

class DummyGate:
    def __init__(self, gate_number, current_flight=None):
        self.gate_number = gate_number
        self.current_flight = current_flight

class DummyTerminal:
    def __init__(self, name, gates):
        self.name = name
        self.gates = gates

class DummyGroundStaff:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class DummyFlight:
    def __init__(self, flight_number):
        self.flight_number = flight_number

@pytest.fixture
def airport():
    return Airport(code="MSQ", name="Minsk National", city="Minsk", country="Belarus")

def test_add_terminal(airport):
    t = DummyTerminal("T1", [])
    airport.add_terminal(t)
    assert airport.terminals == [t]

def test_assign_staff(airport):
    s = DummyGroundStaff("Ivan", "Security")
    airport.assign_staff(s)
    assert airport.staff == [s]

def test_get_terminal_by_name_found(airport):
    t1 = DummyTerminal("T1", [])
    t2 = DummyTerminal("T2", [])
    airport.add_terminal(t1)
    airport.add_terminal(t2)
    assert airport.get_terminal_by_name("T2") == t2

def test_get_terminal_by_name_not_found(airport):
    assert airport.get_terminal_by_name("Ghost") is None

def test_get_all_gates(airport):
    g1 = DummyGate("A1")
    g2 = DummyGate("A2")
    t1 = DummyTerminal("T1", [g1])
    t2 = DummyTerminal("T2", [g2])
    airport.add_terminal(t1)
    airport.add_terminal(t2)
    gates = airport.get_all_gates()
    assert gates == [g1, g2]

def test_find_gate_found(airport):
    g1 = DummyGate("A1")
    t = DummyTerminal("T1", [g1])
    airport.add_terminal(t)
    assert airport.find_gate("A1") == g1

def test_find_gate_not_found(airport):
    t = DummyTerminal("T1", [])
    airport.add_terminal(t)
    assert airport.find_gate("Z9") is None

def test_get_available_gates(airport):
    g1 = DummyGate("A1", current_flight=None)
    g2 = DummyGate("A2", current_flight=DummyFlight("FL123"))
    t = DummyTerminal("T1", [g1, g2])
    airport.add_terminal(t)
    available = airport.get_available_gates()
    assert available == [g1]

def test_get_staff_by_role(airport):
    s1 = DummyGroundStaff("Anna", "Security")
    s2 = DummyGroundStaff("Leo", "Check-in")
    airport.assign_staff(s1)
    airport.assign_staff(s2)
    result = airport.get_staff_by_role("Security")
    assert result == [s1]

def test_has_terminal_true(airport):
    airport.add_terminal(DummyTerminal("T1", []))
    assert airport.has_terminal("T1") is True

def test_has_terminal_false(airport):
    assert airport.has_terminal("Ghost") is False

def test_total_gate_count(airport):
    t1 = DummyTerminal("T1", [DummyGate("A1"), DummyGate("A2")])
    t2 = DummyTerminal("T2", [DummyGate("B1")])
    airport.add_terminal(t1)
    airport.add_terminal(t2)
    assert airport.total_gate_count() == 3

def test_get_flights_departing(airport):
    f1 = DummyFlight("FL001")
    f2 = DummyFlight("FL002")
    g1 = DummyGate("A1", current_flight=f1)
    g2 = DummyGate("A2", current_flight=None)
    g3 = DummyGate("A3", current_flight=f2)
    t = DummyTerminal("T1", [g1, g2, g3])
    airport.add_terminal(t)
    flights = airport.get_flights_departing()
    assert flights == [f1, f2]

def test_summary(airport):
    assert airport.summary() == "Minsk National (MSQ) in Minsk, Belarus"
