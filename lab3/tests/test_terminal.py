import pytest
from models.infrastructure.terminal import Terminal

class DummyGate:
    def __init__(self, gate_number):
        self.gate_number = gate_number

class DummyGroundStaff:
    def __init__(self, name, role):
        self.name = name
        self.role = role

def test_valid_initialization():
    t = Terminal("A")
    assert t.name == "A"
    assert t.gates == []
    assert t.assigned_staff == []
    assert t.maintenance_required is False

def test_invalid_terminal_name():
    with pytest.raises(ValueError, match="Invalid terminal name: Z"):
        Terminal("Z")

@pytest.fixture
def terminal():
    return Terminal("International")

def test_add_gate(terminal):
    g1 = DummyGate("G1")
    terminal.add_gate(g1)
    assert terminal.gates == [g1]

def test_get_gate_by_number_found(terminal):
    g1 = DummyGate("G1")
    g2 = DummyGate("G2")
    terminal.add_gate(g1)
    terminal.add_gate(g2)
    assert terminal.get_gate_by_number("G2") == g2

def test_get_gate_by_number_not_found(terminal):
    assert terminal.get_gate_by_number("X") is None

def test_total_gate_count(terminal):
    terminal.add_gate(DummyGate("G1"))
    terminal.add_gate(DummyGate("G2"))
    assert terminal.total_gate_count() == 2

def test_mark_and_clear_maintenance(terminal):
    terminal.mark_for_maintenance()
    assert terminal.maintenance_required is True
    terminal.clear_maintenance()
    assert terminal.maintenance_required is False

def test_is_operational(terminal):
    assert terminal.is_operational() is True
    terminal.mark_for_maintenance()
    assert terminal.is_operational() is False

def test_assign_staff(terminal):
    s = DummyGroundStaff("Anna", "Security")
    terminal.assign_staff(s)
    assert terminal.assigned_staff == [s]

def test_get_staff_by_role(terminal):
    s1 = DummyGroundStaff("Leo", "Security")
    s2 = DummyGroundStaff("Mira", "Check-in")
    terminal.assign_staff(s1)
    terminal.assign_staff(s2)
    result = terminal.get_staff_by_role("Security")
    assert result == [s1]

def test_summary(terminal):
    terminal.add_gate(DummyGate("G1"))
    terminal.add_gate(DummyGate("G2"))
    assert terminal.summary() == "Terminal International with 2 gates"
