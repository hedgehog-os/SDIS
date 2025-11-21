import pytest
from models.staff.FlightAttendant import FlightAttendant

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

class DummyFlight:
    def __init__(self, flight_number, origin="MSQ", destination="JFK", departure_time="2025-11-07T08:00"):
        self.flight_number = flight_number
        self.route = DummyRoute(DummyAirport(origin), DummyAirport(destination))
        self.schedule = DummySchedule(departure_time)
        self.attendants = []

@pytest.fixture
def attendant():
    return FlightAttendant("Olga", ["English", "Russian", "French"])

def test_assign_to_flight(attendant):
    flight = DummyFlight("SU123")
    attendant.assign_to_flight(flight)
    assert flight in attendant.assigned_flights
    assert attendant in flight.attendants
    assert "Assigned to flight SU123" in attendant.notes

def test_assign_to_flight_duplicate(attendant):
    flight = DummyFlight("SU124")
    attendant.assign_to_flight(flight)
    attendant.assign_to_flight(flight)
    assert attendant.notes.count("Assigned to flight SU124") == 1  # no duplicates

def test_remove_from_flight_success(attendant):
    flight = DummyFlight("SU125")
    attendant.assign_to_flight(flight)
    result = attendant.remove_from_flight(flight)
    assert result is True
    assert flight not in attendant.assigned_flights
    assert attendant not in flight.attendants
    assert "Removed from flight SU125" in attendant.notes

def test_remove_from_flight_failure(attendant):
    flight = DummyFlight("SU126")
    result = attendant.remove_from_flight(flight)
    assert result is False

def test_get_flight_numbers(attendant):
    f1 = DummyFlight("SU127")
    f2 = DummyFlight("SU128")
    attendant.assign_to_flight(f1)
    attendant.assign_to_flight(f2)
    assert attendant.get_flight_numbers() == ["SU127", "SU128"]

def test_get_routes(attendant):
    f1 = DummyFlight("SU129", origin="MSQ", destination="LHR")
    f2 = DummyFlight("SU130", origin="MSQ", destination="CDG")
    attendant.assign_to_flight(f1)
    attendant.assign_to_flight(f2)
    assert attendant.get_routes() == ["MSQ → LHR", "MSQ → CDG"]

def test_get_languages_coverage(attendant):
    assert attendant.get_languages_coverage() == "English, French, Russian"

def test_is_available_for_true(attendant):
    f1 = DummyFlight("SU131", departure_time="2025-11-06T10:00")
    attendant.assign_to_flight(f1)
    assert attendant.is_available_for("2025-11-07") is True

def test_is_available_for_false(attendant):
    f1 = DummyFlight("SU132", departure_time="2025-11-07T10:00")
    attendant.assign_to_flight(f1)
    assert attendant.is_available_for("2025-11-07") is False

def test_get_schedule_summary_empty(attendant):
    assert attendant.get_schedule_summary() == "Olga has no assigned flights."

def test_get_schedule_summary_full(attendant):
    f1 = DummyFlight("SU133", origin="MSQ", destination="FRA", departure_time="2025-11-08T06:00")
    attendant.assign_to_flight(f1)
    summary = attendant.get_schedule_summary()
    assert "Schedule for Olga:" in summary
    assert "• SU133: MSQ → FRA on 2025-11-08T06:00" in summary

def test_to_dict(attendant):
    f1 = DummyFlight("SU134")
    attendant.assign_to_flight(f1)
    d = attendant.to_dict()
    assert d["name"] == "Olga"
    assert "SU134" in d["assigned_flights"]
    assert "Assigned to flight SU134" in d["notes"]
    assert d["languages"] == ["English", "Russian", "French"]
    assert d["notes"] is not attendant.notes  # ensure it's a copy

def test_summary(attendant):
    f1 = DummyFlight("SU135")
    attendant.assign_to_flight(f1)
    summary = attendant.summary()
    assert "Olga — Languages: English, French, Russian" in summary
    assert "Flights: 1 assigned" in summary
