import pytest
from models.infrastructure.runway import Runway

def test_valid_initialization():
    r = Runway("RWY-01", 3000)
    assert r.identifier == "RWY-01"
    assert r.length_meters == 3000
    assert r.is_active is True
    assert r.maintenance_required is False
    assert r.landing_log == []
    assert r.takeoff_log == []

def test_invalid_length_too_short():
    with pytest.raises(ValueError, match="Runway length must be between"):
        Runway("RWY-02", 900)

def test_invalid_length_too_long():
    with pytest.raises(ValueError, match="Runway length must be between"):
        Runway("RWY-03", 6000)

@pytest.fixture
def runway():
    return Runway("RWY-04", 2500)

def test_close_and_open(runway):
    runway.close()
    assert runway.is_active is False
    runway.open()
    assert runway.is_active is True

def test_mark_and_clear_maintenance(runway):
    runway.mark_for_maintenance()
    assert runway.maintenance_required is True
    runway.clear_maintenance()
    assert runway.maintenance_required is False

def test_is_operational(runway):
    assert runway.is_operational() is True
    runway.mark_for_maintenance()
    assert runway.is_operational() is False
    runway.clear_maintenance()
    runway.close()
    assert runway.is_operational() is False

def test_log_landing_and_count(runway):
    runway.log_landing("FL123")
    runway.log_landing("FL456")
    assert runway.landing_log == ["FL123", "FL456"]
    assert runway.get_landing_count() == 2

def test_log_takeoff_and_count(runway):
    runway.log_takeoff("FL789")
    assert runway.takeoff_log == ["FL789"]
    assert runway.get_takeoff_count() == 1

def test_reset(runway):
    runway.log_landing("A")
    runway.log_takeoff("B")
    runway.mark_for_maintenance()
    runway.close()
    runway.reset()
    assert runway.is_active is True
    assert runway.maintenance_required is False
    assert runway.landing_log == []
    assert runway.takeoff_log == []

def test_supports_aircraft_size(runway):
    assert runway.supports_aircraft_size(2000) is True
    assert runway.supports_aircraft_size(2600) is False

def test_summary_active(runway):
    assert runway.summary() == "Runway RWY-04 (2500m, active)"

def test_summary_closed(runway):
    runway.close()
    assert runway.summary() == "Runway RWY-04 (2500m, closed)"
