import pytest
from models.flight.Airline import Airline

class DummyAircraft:
    def __init__(self, model, registration_number, capacity):
        self.model = model
        self.registration_number = registration_number
        self.capacity = capacity

class DummyRoute:
    def __init__(self, destination_code, international=False):
        self.destination = type("Dest", (), {"code": destination_code})
        self._international = international

    def is_international(self):
        return self._international

class DummyFlight:
    def __init__(self, flight_number, route):
        self.flight_number = flight_number
        self.route = route

class DummyPilot:
    def __init__(self, name, license_number):
        self.name = name
        self.license_number = license_number

class DummyAttendant:
    def __init__(self, name, languages):
        self.name = name
        self.languages = languages

class DummyLoyaltyProgram:
    def __init__(self, tier):
        self.tier = tier

@pytest.fixture
def airline():
    return Airline(name="SkyJet", code="SJ", country="Belarus")

def test_full_name(airline):
    assert airline.full_name() == "SkyJet (SJ)"

def test_add_aircraft(airline):
    ac = DummyAircraft("A320", "SJ001", 150)
    airline.add_aircraft(ac)
    assert airline.fleet == [ac]

def test_register_flight(airline):
    flight = DummyFlight("SJ100", DummyRoute("MSQ"))
    airline.register_flight(flight)
    assert airline.flights == [flight]

def test_assign_pilot(airline):
    pilot = DummyPilot("Ivan", "LIC123")
    airline.assign_pilot(pilot)
    assert airline.pilots == [pilot]

def test_assign_attendant(airline):
    attendant = DummyAttendant("Anna", ["English", "Russian"])
    airline.assign_attendant(attendant)
    assert airline.attendants == [attendant]

def test_create_loyalty_program(airline):
    program = DummyLoyaltyProgram("Gold")
    airline.create_loyalty_program(program)
    assert airline.loyalty_programs == [program]

def test_get_aircraft_by_model(airline):
    ac1 = DummyAircraft("A320", "SJ001", 150)
    ac2 = DummyAircraft("B737", "SJ002", 180)
    airline.add_aircraft(ac1)
    airline.add_aircraft(ac2)
    result = airline.get_aircraft_by_model("A320")
    assert result == [ac1]

def test_get_flights_by_destination(airline):
    flight1 = DummyFlight("SJ100", DummyRoute("MSQ"))
    flight2 = DummyFlight("SJ101", DummyRoute("LHR"))
    airline.register_flight(flight1)
    airline.register_flight(flight2)
    result = airline.get_flights_by_destination("LHR")
    assert result == [flight2]

def test_total_seats_available(airline):
    airline.add_aircraft(DummyAircraft("A320", "SJ001", 150))
    airline.add_aircraft(DummyAircraft("B737", "SJ002", 180))
    assert airline.total_seats_available() == 330

def test_is_international_carrier_true(airline):
    flight = DummyFlight("SJ200", DummyRoute("LHR", international=True))
    airline.register_flight(flight)
    assert airline.is_international_carrier() is True

def test_is_international_carrier_false(airline):
    flight = DummyFlight("SJ201", DummyRoute("MSQ", international=False))
    airline.register_flight(flight)
    assert airline.is_international_carrier() is False

def test_get_loyalty_tiers(airline):
    airline.create_loyalty_program(DummyLoyaltyProgram("Silver"))
    airline.create_loyalty_program(DummyLoyaltyProgram("Gold"))
    airline.create_loyalty_program(DummyLoyaltyProgram("Silver"))
    tiers = airline.get_loyalty_tiers()
    assert set(tiers) == {"Silver", "Gold"}

def test_has_aircraft_true(airline):
    ac = DummyAircraft("A320", "SJ001", 150)
    airline.add_aircraft(ac)
    assert airline.has_aircraft("SJ001") is True

def test_has_aircraft_false(airline):
    assert airline.has_aircraft("UNKNOWN") is False

def test_get_pilot_by_license_found(airline):
    pilot = DummyPilot("Ivan", "LIC123")
    airline.assign_pilot(pilot)
    result = airline.get_pilot_by_license("LIC123")
    assert result == pilot

def test_get_pilot_by_license_not_found(airline):
    result = airline.get_pilot_by_license("NOPE")
    assert result is None

def test_get_attendants_by_language(airline):
    a1 = DummyAttendant("Anna", ["English", "Russian"])
    a2 = DummyAttendant("John", ["French"])
    airline.assign_attendant(a1)
    airline.assign_attendant(a2)
    result = airline.get_attendants_by_language("Russian")
    assert result == [a1]
