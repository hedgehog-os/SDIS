import pytest
from models.flight.flight import Flight
from exceptions.flight_exceptions import GateConflictException

# Dummy classes
class DummyPassport:
    def __init__(self, number): self.number = number

class DummyTicket:
    def __init__(self, code): self.code = code

class DummyPassenger:
    def __init__(self, name, passport_number, ticket_code):
        self.full_name = name
        self.passport = DummyPassport(passport_number)
        self.ticket = DummyTicket(ticket_code)

class DummyBoardingPass:
    def __init__(self, ticket, passenger, gate_number):
        self.ticket = ticket
        self.passenger = passenger
        self.gate_number = gate_number

class DummyAircraft:
    def __init__(self, model, capacity):
        self.model = model
        self.capacity = capacity

class DummyGate:
    def __init__(self, gate_number):
        self.gate_number = gate_number
        self.current_flight = None
    def assign_flight(self, flight): self.current_flight = flight

class DummyRoute:
    def __init__(self, origin, destination):
        self.origin = type("Origin", (), {"code": origin})
        self.destination = type("Dest", (), {"code": destination})

class DummySchedule:
    def __init__(self, dep, arr, valid=True):
        self.departure_time = dep
        self.arrival_time = arr
        self._valid = valid
    def is_valid_range(self): return self._valid

class DummyPilot:
    def __init__(self, name): self.name = name

class DummyAttendant:
    def __init__(self, name, languages):
        self.name = name
        self.languages = languages

class DummyAirline:
    def __init__(self, name): self.name = name

@pytest.fixture
def flight():
    return Flight(
        flight_number="FL123",
        airline=DummyAirline("SkyJet"),
        aircraft=DummyAircraft("A320", 2),
        route=DummyRoute("MSQ", "LHR"),
        schedule=DummySchedule("2025-11-06 10:00", "2025-11-06 12:00"),
        departure_gate=DummyGate("A1"),
        arrival_gate=DummyGate("B2")
    )

def test_board_passenger_success(flight):
    p = DummyPassenger("Alice", "P123", "T001")
    flight.board_passenger(p)
    assert flight.passengers == [p]
    assert "Boarded Alice" in flight.notes

def test_board_passenger_full(flight):
    flight.board_passenger(DummyPassenger("A", "P1", "T1"))
    flight.board_passenger(DummyPassenger("B", "P2", "T2"))
    with pytest.raises(Exception, match="Flight is full."):
        flight.board_passenger(DummyPassenger("C", "P3", "T3"))

def test_remove_passenger_success(flight):
    p = DummyPassenger("Bob", "P456", "T002")
    flight.board_passenger(p)
    assert flight.remove_passenger("P456") is True
    assert "Removed passenger Bob" in flight.notes

def test_remove_passenger_not_found(flight):
    assert flight.remove_passenger("UNKNOWN") is False

def test_get_manifest(flight):
    p1 = DummyPassenger("A", "P1", "T1")
    p2 = DummyPassenger("B", "P2", "T2")
    flight.board_passenger(p1)
    flight.board_passenger(p2)
    manifest = flight.get_manifest()
    assert manifest == [p1, p2]
    assert manifest is not flight.passengers  # copy check

def test_is_full_and_available_seats(flight):
    assert flight.is_full() is False
    assert flight.available_seats() == 2
    flight.board_passenger(DummyPassenger("A", "P1", "T1"))
    flight.board_passenger(DummyPassenger("B", "P2", "T2"))
    assert flight.is_full() is True
    assert flight.available_seats() == 0

def test_has_passenger(flight):
    p = DummyPassenger("C", "P789", "T003")
    flight.board_passenger(p)
    assert flight.has_passenger("P789") is True
    assert flight.has_passenger("NOPE") is False

def test_assign_gate_success(flight):
    new_gate = DummyGate("C3")
    flight.assign_gate(new_gate)
    assert flight.departure_gate == new_gate
    assert new_gate.current_flight == flight
    assert "Gate C3 assigned" in flight.notes

def test_assign_gate_conflict(flight):
    other_flight = Flight(
        "FL999", DummyAirline("Other"), DummyAircraft("B737", 100),
        DummyRoute("AAA", "BBB"), DummySchedule("2025-11-06 10:00", "2025-11-06 12:00"),
        DummyGate("X1"), DummyGate("X2")
    )
    conflict_gate = DummyGate("Z9")
    conflict_gate.current_flight = other_flight
    with pytest.raises(GateConflictException):
        flight.assign_gate(conflict_gate)

def test_get_passenger_by_name(flight):
    p = DummyPassenger("Diana", "P321", "T004")
    flight.board_passenger(p)
    assert flight.get_passenger_by_name("Diana") == p
    assert flight.get_passenger_by_name("Ghost") is None

def test_assign_crew(flight):
    pilot = DummyPilot("Captain Jack")
    attendants = [DummyAttendant("Anna", ["English"]), DummyAttendant("Leo", ["French"])]
    flight.assign_crew(pilot, attendants)
    assert flight.pilots == [pilot]
    assert flight.attendants == attendants
    assert "Crew assigned: Pilot Captain Jack, 2 attendants" in flight.notes

def test_get_languages_onboard(flight):
    attendants = [DummyAttendant("A", ["English", "Spanish"]), DummyAttendant("B", ["Spanish", "French"])]
    flight.assign_crew(DummyPilot("P"), attendants)
    langs = flight.get_languages_onboard()
    assert set(langs) == {"English", "Spanish", "French"}


def test_is_ready_for_departure(flight):
    flight.assign_crew(DummyPilot("P"), [DummyAttendant("A", ["English"]), DummyAttendant("B", ["French"])])
    assert flight.is_ready_for_departure() is True
    flight.board_passenger(DummyPassenger("X", "P1", "T1"))
    flight.board_passenger(DummyPassenger("Y", "P2", "T2"))
    assert flight.is_ready_for_departure() is False  # full

def test_update_status(flight):
    flight.update_status("Boarding")
    assert flight.status == "Boarding"
    assert "Status updated to Boarding" in flight.notes

def test_get_flight_summary(flight):
    flight.board_passenger(DummyPassenger("A", "P1", "T1"))
    summary = flight.get_flight_summary()
    assert "FL123: MSQ → LHR" in summary
    assert "1/2 passengers" in summary
    assert "Status: Scheduled" in summary

def test_to_dict(flight):
    flight.assign_crew(DummyPilot("P"), [DummyAttendant("A", ["English"])])
    flight.board_passenger(DummyPassenger("A", "P1", "T1"))
    flight.update_status("Boarding")
    d = flight.to_dict()
    assert d["flight_number"] == "FL123"
    assert d["airline"] == "SkyJet"
    assert d["aircraft"] == "A320"
    assert d["route"] == "MSQ → LHR"
    assert d["status"] == "Boarding"
    assert d["passenger_count"] == 1
    assert d["crew"]["pilots"] == ["P"]
    assert d["crew"]["attendants"] == ["A"]
    assert d["boarding_passes"] == []  # boarding passes not generated yet
    assert isinstance(d["notes"], list)
    assert "Status updated to Boarding" in d["notes"]

def test_is_ready_for_departure_insufficient_attendants(flight):
    flight.assign_crew(DummyPilot("P"), [DummyAttendant("A", ["English"])])  # only 1 attendant
    assert flight.is_ready_for_departure() is False

def test_is_ready_for_departure_invalid_schedule(flight):
    flight.schedule._valid = False
    flight.assign_crew(DummyPilot("P"), [DummyAttendant("A", ["English"]), DummyAttendant("B", ["French"])])
    assert flight.is_ready_for_departure() is False

