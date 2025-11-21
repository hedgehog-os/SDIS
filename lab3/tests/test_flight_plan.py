import pytest
from models.operations.FlightPlan import FlightPlan

class DummyRoute:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

class DummyAircraft:
    def __init__(self, registration, max_altitude_ft, fuel_burn_rate_per_min):
        self.registration = registration
        self.max_altitude_ft = max_altitude_ft
        self.fuel_burn_rate_per_min = fuel_burn_rate_per_min

def test_valid_initialization():
    route = DummyRoute("Minsk", "Berlin")
    aircraft = DummyAircraft("EW-001", 41000, 5.2)
    fp = FlightPlan(route, aircraft, 35000, 120)
    assert fp.route == route
    assert fp.aircraft == aircraft
    assert fp.cruising_altitude_ft == 35000
    assert fp.estimated_duration_min == 120
    assert fp.is_approved is False
    assert fp.notes == []

def test_invalid_altitude_low():
    route = DummyRoute("A", "B")
    aircraft = DummyAircraft("X", 40000, 5.0)
    with pytest.raises(ValueError, match="Cruising altitude must be between"):
        FlightPlan(route, aircraft, 9000, 60)

def test_invalid_altitude_high():
    route = DummyRoute("A", "B")
    aircraft = DummyAircraft("X", 40000, 5.0)
    with pytest.raises(ValueError, match="Cruising altitude must be between"):
        FlightPlan(route, aircraft, 46000, 60)

def test_invalid_duration():
    route = DummyRoute("A", "B")
    aircraft = DummyAircraft("X", 40000, 5.0)
    with pytest.raises(ValueError, match="Estimated duration must be positive."):
        FlightPlan(route, aircraft, 30000, 0)

@pytest.fixture
def flight_plan():
    route = DummyRoute("Paris", "Rome")
    aircraft = DummyAircraft("FR-007", 39000, 4.5)
    return FlightPlan(route, aircraft, 35000, 100)

def test_approve(flight_plan):
    flight_plan.approve()
    assert flight_plan.is_approved is True

def test_reject(flight_plan):
    flight_plan.reject("Weather conditions")
    assert flight_plan.is_approved is False
    assert flight_plan.notes == ["Rejected: Weather conditions"]

def test_add_note(flight_plan):
    flight_plan.add_note("Check alternate route")
    assert flight_plan.notes == ["Check alternate route"]

def test_reset(flight_plan):
    flight_plan.approve()
    flight_plan.add_note("Initial approval")
    flight_plan.reset()
    assert flight_plan.is_approved is False
    assert flight_plan.notes == []

def test_summary_pending(flight_plan):
    summary = flight_plan.summary()
    assert summary == "FlightPlan for FR-007 via Paris → Rome, 35000 ft, 100 min, PENDING"

def test_summary_approved(flight_plan):
    flight_plan.approve()
    assert "APPROVED" in flight_plan.summary()

def test_is_suitable_for_aircraft_true(flight_plan):
    assert flight_plan.is_suitable_for_aircraft() is True

def test_is_suitable_for_aircraft_false():
    route = DummyRoute("X", "Y")
    aircraft = DummyAircraft("LOW", 30000, 6.0)
    fp = FlightPlan(route, aircraft, 35000, 90)
    assert fp.is_suitable_for_aircraft() is False

def test_estimated_fuel_usage(flight_plan):
    expected = round(4.5 * 100, 2)
    assert flight_plan.estimated_fuel_usage() == expected
