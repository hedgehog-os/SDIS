import pytest
from models.flight.Route import Route

class DummyAirport:
    def __init__(self, code, city, country):
        self.code = code
        self.city = city
        self.country = country

@pytest.fixture
def domestic_route():
    origin = DummyAirport("MSQ", "Minsk", "Belarus")
    destination = DummyAirport("GME", "Gomel", "Belarus")
    return Route(origin, destination, 300)

@pytest.fixture
def international_route():
    origin = DummyAirport("MSQ", "Minsk", "Belarus")
    destination = DummyAirport("LHR", "London", "UK")
    return Route(origin, destination, 2200)

def test_is_international(international_route, domestic_route):
    assert international_route.is_international() is True
    assert domestic_route.is_international() is False

def test_is_domestic(international_route, domestic_route):
    assert domestic_route.is_domestic() is True
    assert international_route.is_domestic() is False

def test_is_short_haul(domestic_route, international_route):
    assert domestic_route.is_short_haul() is True
    assert international_route.is_short_haul() is False

def test_is_long_haul():
    origin = DummyAirport("MSQ", "Minsk", "Belarus")
    destination = DummyAirport("JFK", "New York", "USA")
    route = Route(origin, destination, 7200)
    assert route.is_long_haul() is True

def test_is_long_haul_false(international_route):
    assert international_route.is_long_haul() is False

def test_midpoint_city(international_route):
    assert international_route.midpoint_city() == "Minsk–London"

def test_add_and_check_alternate_airport(international_route):
    alt = DummyAirport("CDG", "Paris", "France")
    international_route.add_alternate_airport(alt)
    assert international_route.has_alternate_airport("CDG") is True
    assert international_route.has_alternate_airport("FRA") is False

def test_get_country_pair(international_route):
    assert international_route.get_country_pair() == ("Belarus", "UK")

def test_get_airport_codes(international_route):
    assert international_route.get_airport_codes() == ("MSQ", "LHR")

def test_summary(international_route):
    assert international_route.summary() == "MSQ → LHR (2200 km)"
