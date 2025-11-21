import pytest
from models.operations.WeatherReport import WeatherReport

class DummyAircraft:
    def __init__(self, registration, min_operating_temp_c, max_crosswind_kph):
        self.registration = registration
        self.min_operating_temp_c = min_operating_temp_c
        self.max_crosswind_kph = max_crosswind_kph

class DummyRunway:
    def __init__(self, code, is_flooded=False, is_icy=False):
        self.code = code
        self.is_flooded = is_flooded
        self.is_icy = is_icy

def test_initialization():
    report = WeatherReport("Minsk", 10.0, 20.0, "Clear")
    assert report.location == "Minsk"
    assert report.temperature_c == 10.0
    assert report.wind_kph == 20.0
    assert report.condition == "clear"
    assert report.aircraft is None
    assert report.runway is None
    assert report.notes == []
    assert report.is_verified is False

@pytest.mark.parametrize("condition", ["storm", "fog", "snow", "hail", "tornado"])
def test_unsafe_conditions(condition):
    report = WeatherReport("Minsk", 15.0, 20.0, condition)
    assert report.is_safe_for_flight() is False

def test_extreme_wind():
    report = WeatherReport("Minsk", 15.0, 65.0, "clear")
    assert report.is_safe_for_flight() is False

def test_extreme_temperature_low():
    report = WeatherReport("Minsk", -35.0, 10.0, "clear")
    assert report.is_safe_for_flight() is False

def test_extreme_temperature_high():
    report = WeatherReport("Minsk", 50.0, 10.0, "clear")
    assert report.is_safe_for_flight() is False

def test_safe_for_aircraft_true():
    aircraft = DummyAircraft("EW-001", -20.0, 30.0)
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", aircraft=aircraft)
    assert report.is_safe_for_aircraft() is True

def test_safe_for_aircraft_false_due_to_temp():
    aircraft = DummyAircraft("EW-002", 10.0, 30.0)
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", aircraft=aircraft)
    assert report.is_safe_for_aircraft() is False

def test_safe_for_aircraft_false_due_to_wind():
    aircraft = DummyAircraft("EW-003", -20.0, 20.0)
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", aircraft=aircraft)
    assert report.is_safe_for_aircraft() is False

def test_safe_for_runway_true():
    runway = DummyRunway("RW-01", is_flooded=False, is_icy=False)
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", runway=runway)
    assert report.is_safe_for_runway() is True

def test_safe_for_runway_false_flooded():
    runway = DummyRunway("RW-02", is_flooded=True)
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", runway=runway)
    assert report.is_safe_for_runway() is False

def test_safe_for_runway_false_icy():
    runway = DummyRunway("RW-03", is_icy=True)
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", runway=runway)
    assert report.is_safe_for_runway() is False

def test_mark_verified():
    report = WeatherReport("Minsk", 5.0, 25.0, "clear")
    report.mark_verified()
    assert report.is_verified is True

def test_add_note():
    report = WeatherReport("Minsk", 5.0, 25.0, "clear")
    report.add_note("Visibility good")
    assert report.notes == ["Visibility good"]

def test_reset():
    report = WeatherReport("Minsk", 5.0, 25.0, "clear")
    report.mark_verified()
    report.add_note("Initial check")
    report.reset()
    assert report.notes == []
    assert report.is_verified is False

def test_summary_safe_verified():
    aircraft = DummyAircraft("EW-004", -20.0, 30.0)
    runway = DummyRunway("RW-04")
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", aircraft=aircraft, runway=runway)
    report.mark_verified()
    summary = report.summary()
    assert "SAFE" in summary
    assert "VERIFIED" in summary
    assert "EW-004" in summary
    assert "RW-04" in summary

def test_summary_unsafe_unverified():
    aircraft = DummyAircraft("EW-005", 10.0, 30.0)
    runway = DummyRunway("RW-05", is_icy=True)
    report = WeatherReport("Minsk", 5.0, 25.0, "clear", aircraft=aircraft, runway=runway)
    summary = report.summary()
    assert "UNSAFE" in summary
    assert "UNVERIFIED" in summary
