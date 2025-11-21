import pytest
from models.staff.GroundStaff import GroundStaff

class DummyAirport:
    def __init__(self, code):
        self.code = code

class DummyGate:
    def __init__(self, gate_number):
        self.gate_number = gate_number

class DummyFlight:
    def __init__(self, flight_number):
        self.flight_number = flight_number

class DummyRestroom:
    def __init__(self, location_id):
        self.location_id = location_id
        self.is_clean = False

class DummyLounge:
    def __init__(self, name):
        self.name = name
        self.is_clean = False

@pytest.fixture
def staff():
    return GroundStaff("Ivan", "Coordinator", DummyAirport("MSQ"))

def test_assign_gate(staff):
    gate = DummyGate("G1")
    staff.assign_gate(gate)
    assert gate in staff.assigned_gates
    assert "Assigned to gate G1" in staff.notes

def test_assign_gate_duplicate(staff):
    gate = DummyGate("G2")
    staff.assign_gate(gate)
    staff.assign_gate(gate)
    assert staff.assigned_gates.count(gate) == 1

def test_perform_task(staff):
    staff.perform_task("Security check", "Gate G3")
    assert "Security check" in staff.assigned_tasks
    assert staff.task_log[-1]["location"] == "Gate G3"
    assert "Performed 'Security check' at Gate G3" in staff.notes[-1]

def test_assist_flight(staff):
    flight = DummyFlight("SU123")
    staff.assist_flight(flight)
    assert "Flight assistance" in staff.assigned_tasks
    assert staff.task_log[-1]["location"] == "SU123"

def test_clean_area_restroom(staff):
    restroom = DummyRestroom("R101")
    staff.clean_area(restroom)
    assert restroom.is_clean is True
    assert "Cleaning" in staff.assigned_tasks
    assert "R101" in staff.task_log[-1]["location"]

def test_clean_area_lounge(staff):
    lounge = DummyLounge("VIP Lounge")
    staff.clean_area(lounge)
    assert lounge.is_clean is True
    assert "VIP Lounge" in staff.task_log[-1]["location"]

def test_get_gate_numbers(staff):
    g1 = DummyGate("G1")
    g2 = DummyGate("G2")
    staff.assign_gate(g1)
    staff.assign_gate(g2)
    assert staff.get_gate_numbers() == ["G1", "G2"]

def test_get_task_summary_empty(staff):
    assert staff.get_task_summary() == "Ivan has no recorded tasks."

def test_get_task_summary_full(staff):
    staff.perform_task("Boarding", "Gate G4")
    summary = staff.get_task_summary()
    assert "Task log for Ivan:" in summary
    assert "• Boarding at Gate G4" in summary

def test_reset_tasks(staff):
    staff.perform_task("Check documents", "Gate G5")
    staff.reset_tasks()
    assert staff.assigned_tasks == []
    assert staff.task_log == []
    assert "Reset 1 task(s) for new shift" in staff.notes[-1]

def test_to_dict(staff):
    gate = DummyGate("G6")
    staff.assign_gate(gate)
    staff.perform_task("Escort", "Gate G6")
    d = staff.to_dict()
    assert d["name"] == "Ivan"
    assert d["role"] == "Coordinator"
    assert d["airport"] == "MSQ"
    assert d["assigned_gates"] == ["G6"]
    assert "Escort" in d["tasks"]
    assert d["notes"] is not staff.notes  # ensure it's a copy

def test_summary(staff):
    staff.assign_gate(DummyGate("G7"))
    staff.perform_task("Help wheelchair", "Gate G7")
    summary = staff.summary()
    assert "Ivan — Role: Coordinator, Airport: MSQ" in summary
    assert "Gates: 1" in summary
    assert "Tasks: 1" in summary
