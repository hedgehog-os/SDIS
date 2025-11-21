import pytest
from models.staff.Pilot import Pilot

class DummyAirport:
    def __init__(self, code):
        self.code = code

class DummyRoute:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

class DummySchedule:
    def __init__(self, departure_time):
        self.departure_time = departure_time

class DummyAircraft:
    def __init__(self, model):
        self.model = model

class DummyFlight:
    def __init__(self, flight_number, model="A320", origin="MSQ", destination="JFK", departure_time="2025-11-07T08:00"):
        self.flight_number = flight_number
        self.aircraft = DummyAircraft(model)
        self.route = DummyRoute(DummyAirport(origin), DummyAirport(destination))
        self.schedule = DummySchedule(departure_time)
        self.pilots = []

@pytest.fixture
def pilot():
    return Pilot("Sergey", "LIC-001", 12)

def test_assign_flight(pilot):
    flight = DummyFlight("SU123")
    pilot.assign_flight(flight)
    assert flight in pilot.assigned_flights
    assert pilot in flight.pilots
    assert "Assigned to flight SU123" in pilot.notes
    assert pilot.flight_log[-1]["flight"] == "SU123"

def test_assign_flight_duplicate(pilot):
    flight = DummyFlight("SU124")
    pilot.assign_flight(flight)
    pilot.assign_flight(flight)
    assert pilot.assigned_flights.count(flight) == 1

def test_is_certified_for_true(pilot):
    pilot.certifications.append("A320")
    aircraft = DummyAircraft("A320")
    assert pilot.is_certified_for(aircraft) is True

def test_is_certified_for_false(pilot):
    aircraft = DummyAircraft("B737")
    assert pilot.is_certified_for(aircraft) is False

def test_add_certification(pilot):
    pilot.add_certification("B737")
    assert "B737" in pilot.certifications
    assert "Certified for B737" in pilot.notes

def test_add_certification_duplicate(pilot):
    pilot.add_certification("A320")
    pilot.add_certification("A320")
    assert pilot.certifications.count("A320") == 1

def test_remove_certification(pilot):
    pilot.certifications = ["A320", "B737"]
    pilot.remove_certification("A320")
    assert "A320" not in pilot.certifications
    assert "Certification removed for A320" in pilot.notes

def test_remove_certification_not_present(pilot):
    pilot.remove_certification("A350")
    assert "Certification removed for A350" not in pilot.notes

def test_get_flight_numbers(pilot):
    f1 = DummyFlight("SU125")
    f2 = DummyFlight("SU126")
    pilot.assign_flight(f1)
    pilot.assign_flight(f2)
    assert pilot.get_flight_numbers() == ["SU125", "SU126"]

def test_get_certification_summary(pilot):
    pilot.certifications = ["A320", "B737"]
    summary = pilot.get_certification_summary()
    assert summary == "A320, B737" or summary == "B737, A320"

def test_get_certification_summary_empty(pilot):
    assert pilot.get_certification_summary() == "None"

def test_get_schedule_summary_empty(pilot):
    assert pilot.get_schedule_summary() == "Sergey has no assigned flights."

def test_get_schedule_summary_full(pilot):
    f1 = DummyFlight("SU127", origin="MSQ", destination="LHR", departure_time="2025-11-08T06:00")
    pilot.assign_flight(f1)
    summary = pilot.get_schedule_summary()
    assert "Schedule for Sergey:" in summary
    assert "• SU127: MSQ → LHR on 2025-11-08T06:00" in summary

def test_reset_schedule(pilot):
    f1 = DummyFlight("SU128")
    pilot.assign_flight(f1)
    pilot.reset_schedule()
    assert pilot.assigned_flights == []
    assert "Reset schedule with 1 flights" in pilot.notes[-1]

def test_to_dict(pilot):
    f1 = DummyFlight("SU129")
    pilot.add_certification("A320")
    pilot.assign_flight(f1)
    d = pilot.to_dict()
    assert d["name"] == "Sergey"
    assert d["license_number"] == "LIC-001"
    assert d["experience_years"] == 12
    assert "SU129" in d["assigned_flights"]
    assert "A320" in d["certifications"]
    assert d["notes"] is not pilot.notes  # ensure it's a copy

def test_summary(pilot):
    pilot.add_certification("A320")
    f1 = DummyFlight("SU130")
    pilot.assign_flight(f1)
    summary = pilot.summary()
    assert "Sergey — License: LIC-001" in summary
    assert "Experience: 12 years" in summary
    assert "Certified for: A320" in summary
    assert "Flights assigned: 1" in summary
