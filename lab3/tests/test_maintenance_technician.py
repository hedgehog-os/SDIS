import pytest
from models.staff.MaintenanceTechnician import MaintenanceTechnician

class DummyAircraft:
    def __init__(self, registration_number, model):
        self.registration_number = registration_number
        self.model = model
        self.last_inspection_by = None
        self.maintenance_records = []

    def mark_maintenance(self, task, technician_name, timestamp):
        self.maintenance_records.append((task, technician_name, timestamp))

@pytest.fixture
def technician():
    return MaintenanceTechnician("Alexei", "Avionics")

def test_inspect_aircraft(technician):
    aircraft = DummyAircraft("EW-001", "A320")
    msg = technician.inspect_aircraft(aircraft)
    assert "Alexei inspected aircraft EW-001 (A320)" in msg
    assert "EW-001" in technician.inspected_aircrafts
    assert "Inspected EW-001 (A320)" in technician.notes[-1]
    assert aircraft.last_inspection_by == "Alexei"

def test_perform_maintenance(technician):
    aircraft = DummyAircraft("EW-002", "B737")
    technician.perform_maintenance(aircraft, "Hydraulic check")
    assert "Performed 'Hydraulic check' on EW-002" in technician.notes[-1]
    assert technician.maintenance_log[-1]["action"] == "Maintenance: Hydraulic check"
    assert aircraft.maintenance_records[-1][0] == "Hydraulic check"
    assert aircraft.maintenance_records[-1][1] == "Alexei"

def test_get_aircrafts_serviced(technician):
    a1 = DummyAircraft("EW-003", "A220")
    a2 = DummyAircraft("EW-004", "A320")
    technician.perform_maintenance(a1, "Oil change")
    technician.perform_maintenance(a2, "Brake test")
    technician.perform_maintenance(a1, "Tire pressure")
    serviced = technician.get_aircrafts_serviced()
    assert set(serviced) == {"EW-003", "EW-004"}

def test_get_log_summary_empty(technician):
    assert technician.get_log_summary() == "Alexei has no recorded maintenance activity."

def test_get_log_summary_full(technician):
    a = DummyAircraft("EW-005", "A321")
    technician.inspect_aircraft(a)
    technician.perform_maintenance(a, "Engine check")
    summary = technician.get_log_summary()
    assert "Maintenance log for Alexei:" in summary
    assert "• Inspection on EW-005" in summary
    assert "• Maintenance: Engine check on EW-005" in summary

def test_reset_log(technician):
    a = DummyAircraft("EW-006", "B777")
    technician.inspect_aircraft(a)
    technician.perform_maintenance(a, "Fuel system")
    technician.reset_log()
    assert technician.maintenance_log == []
    assert technician.inspected_aircrafts == []
    assert "Reset log with 2 entries" in technician.notes[-1]

def test_to_dict(technician):
    a = DummyAircraft("EW-007", "A350")
    technician.inspect_aircraft(a)
    d = technician.to_dict()
    assert d["name"] == "Alexei"
    assert d["specialization"] == "Avionics"
    assert "EW-007" in d["inspected_aircrafts"]
    assert d["notes"] is not technician.notes  # ensure it's a copy

def test_summary(technician):
    a = DummyAircraft("EW-008", "B787")
    technician.perform_maintenance(a, "Landing gear")
    summary = technician.summary()
    assert "Alexei — Specialization: Avionics" in summary
    assert "Aircrafts serviced: 1" in summary
    assert "Total tasks: 1" in summary
