import pytest
from models.flight.aircraft import Aircraft

class DummyTechnician:
    def __init__(self, name):
        self.name = name

class DummyMaintenanceLog:
    def __init__(self, technician):
        self.technician = technician

class DummyFuelRecord:
    def __init__(self, fuel_liters):
        self.fuel_liters = fuel_liters

class DummyFlight:
    def __init__(self, flight_number):
        self.flight_number = flight_number

@pytest.fixture
def aircraft():
    return Aircraft(model="Boeing 737", registration_number="N12345", capacity=180)

def test_valid_registration_prefix_N(aircraft):
    assert aircraft.is_valid_registration() is True

def test_valid_registration_alpha_prefix():
    ac = Aircraft("Airbus A320", "AB9876", 150)
    assert ac.is_valid_registration() is True

def test_invalid_registration():
    ac = Aircraft("CRJ", "123456", 50)
    assert ac.is_valid_registration() is False

def test_assign_flight(aircraft):
    flight = DummyFlight("FL123")
    aircraft.assign_flight(flight)
    assert aircraft.assigned_flights == [flight]

def test_get_last_flight_none(aircraft):
    assert aircraft.get_last_flight() is None

def test_get_last_flight_after_assignment(aircraft):
    flight1 = DummyFlight("FL001")
    flight2 = DummyFlight("FL002")
    aircraft.assign_flight(flight1)
    aircraft.assign_flight(flight2)
    assert aircraft.get_last_flight() == flight2

def test_log_maintenance(aircraft):
    tech = DummyTechnician("Alex")
    log = DummyMaintenanceLog(technician=tech)
    aircraft.log_maintenance(log)
    assert aircraft.maintenance_logs == [log]

def test_last_maintenance_none(aircraft):
    assert aircraft.last_maintenance() is None

def test_last_maintenance_after_logging(aircraft):
    tech = DummyTechnician("Sam")
    log1 = DummyMaintenanceLog(technician=tech)
    log2 = DummyMaintenanceLog(technician=tech)
    aircraft.log_maintenance(log1)
    aircraft.log_maintenance(log2)
    assert aircraft.last_maintenance() == log2

def test_was_inspected_by_true(aircraft):
    tech = DummyTechnician("Dana")
    log = DummyMaintenanceLog(technician=tech)
    aircraft.log_maintenance(log)
    assert aircraft.was_inspected_by(tech) is True

def test_was_inspected_by_false(aircraft):
    tech1 = DummyTechnician("A")
    tech2 = DummyTechnician("B")
    log = DummyMaintenanceLog(technician=tech1)
    aircraft.log_maintenance(log)
    assert aircraft.was_inspected_by(tech2) is False

def test_refuel(aircraft):
    record = DummyFuelRecord(500.0)
    aircraft.refuel(record)
    assert aircraft.fuel_records == [record]

def test_total_fuel_loaded_empty(aircraft):
    assert aircraft.total_fuel_loaded() == 0.0

def test_total_fuel_loaded_multiple(aircraft):
    aircraft.refuel(DummyFuelRecord(300.0))
    aircraft.refuel(DummyFuelRecord(200.0))
    assert aircraft.total_fuel_loaded() == 500.0

def test_is_overbooked_false(aircraft):
    assert aircraft.is_overbooked(100) is False

def test_is_overbooked_true(aircraft):
    assert aircraft.is_overbooked(200) is True

def test_summary(aircraft):
    assert aircraft.summary() == "Boeing 737 (N12345)"
