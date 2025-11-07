import pytest
from models.infrastructure.kiosk import Kiosk

def test_valid_initialization():
    kiosk = Kiosk("K1", "arrival hall")
    assert kiosk.kiosk_id == "K1"
    assert kiosk.location == "arrival hall"
    assert kiosk.is_active is True
    assert kiosk.maintenance_required is False
    assert kiosk.usage_log == []
    assert kiosk.error_log == []

def test_invalid_location():
    with pytest.raises(ValueError, match="Invalid location: unknown zone"):
        Kiosk("K2", "unknown zone")

@pytest.fixture
def kiosk():
    return Kiosk("K3", "main lobby")

def test_deactivate_and_activate(kiosk):
    kiosk.deactivate()
    assert kiosk.is_active is False
    kiosk.activate()
    assert kiosk.is_active is True

def test_mark_and_clear_maintenance(kiosk):
    kiosk.mark_for_maintenance()
    assert kiosk.maintenance_required is True
    kiosk.clear_maintenance()
    assert kiosk.maintenance_required is False

def test_log_usage(kiosk):
    kiosk.log_usage("user123")
    kiosk.log_usage("user456")
    assert kiosk.usage_log == ["user123", "user456"]
    assert kiosk.usage_count() == 2

def test_log_error(kiosk):
    kiosk.log_error("Screen frozen")
    assert kiosk.error_log == ["Screen frozen"]
    assert kiosk.maintenance_required is True
    assert kiosk.error_count() == 1

def test_reset(kiosk):
    kiosk.log_usage("user1")
    kiosk.log_error("Error A")
    kiosk.deactivate()
    kiosk.mark_for_maintenance()
    kiosk.reset()
    assert kiosk.is_active is True
    assert kiosk.maintenance_required is False
    assert kiosk.usage_log == []
    assert kiosk.error_log == []

def test_is_operational(kiosk):
    assert kiosk.is_operational() is True
    kiosk.mark_for_maintenance()
    assert kiosk.is_operational() is False
    kiosk.clear_maintenance()
    kiosk.deactivate()
    assert kiosk.is_operational() is False

def test_get_location_zone(kiosk):
    assert kiosk.get_location_zone() == "MAIN_LOBBY"
