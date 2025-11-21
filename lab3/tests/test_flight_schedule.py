import pytest
from datetime import datetime, timedelta
from models.flight.FlightSchedule import FlightSchedule

@pytest.fixture
def schedule():
    return FlightSchedule(
        departure_time="2025-11-06 14:00",
        arrival_time="2025-11-06 18:30"
    )

def test_duration_minutes(schedule):
    assert schedule.duration_minutes() == 270

def test_overlaps_with_true():
    s1 = FlightSchedule("2025-11-06 10:00", "2025-11-06 12:00")
    s2 = FlightSchedule("2025-11-06 11:00", "2025-11-06 13:00")
    assert s1.overlaps_with(s2) is True

def test_overlaps_with_false():
    s1 = FlightSchedule("2025-11-06 08:00", "2025-11-06 09:00")
    s2 = FlightSchedule("2025-11-06 10:00", "2025-11-06 11:00")
    assert s1.overlaps_with(s2) is False

def test_assign_flight(schedule):
    class DummyFlight:
        def __init__(self, number): self.flight_number = number
    flight = DummyFlight("AB123")
    schedule.assign_flight(flight)
    assert schedule.associated_flight == flight

def test_is_night_flight_true_late():
    s = FlightSchedule("2025-11-06 23:45", "2025-11-07 02:00")
    assert s.is_night_flight() is True

def test_is_night_flight_true_early():
    s = FlightSchedule("2025-11-06 05:30", "2025-11-06 07:00")
    assert s.is_night_flight() is True

def test_is_night_flight_false():
    s = FlightSchedule("2025-11-06 10:00", "2025-11-06 12:00")
    assert s.is_night_flight() is False

def test_is_long_haul_true():
    s = FlightSchedule("2025-11-06 08:00", "2025-11-06 15:30")
    assert s.is_long_haul() is True

def test_is_long_haul_false(schedule):
    assert schedule.is_long_haul() is False

def test_shift_by_minutes_forward(schedule):
    schedule.shift_by_minutes(30)
    assert schedule.departure_time == "2025-11-06 14:30"
    assert schedule.arrival_time == "2025-11-06 19:00"

def test_shift_by_minutes_backward(schedule):
    schedule.shift_by_minutes(-60)
    assert schedule.departure_time == "2025-11-06 13:00"
    assert schedule.arrival_time == "2025-11-06 17:30"

def test_is_departing_today_true():
    today = datetime.today().strftime("%Y-%m-%d")
    s = FlightSchedule(f"{today} 09:00", f"{today} 12:00")
    assert s.is_departing_today() is True

def test_is_departing_today_false():
    s = FlightSchedule("2025-01-01 10:00", "2025-01-01 12:00")
    assert s.is_departing_today() is False

def test_get_day_of_week():
    s = FlightSchedule("2025-11-06 10:00", "2025-11-06 12:00")
    assert s.get_day_of_week() == "Thursday"

def test_is_valid_range_true(schedule):
    assert schedule.is_valid_range() is True

def test_is_valid_range_false():
    s = FlightSchedule("2025-11-06 18:00", "2025-11-06 17:00")
    assert s.is_valid_range() is False
