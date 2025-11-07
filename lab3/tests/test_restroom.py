import pytest
from models.infrastructure.restroom import Restroom

def test_valid_initialization():
    r = Restroom("arrival hall", is_accessible=True)
    assert r.location == "arrival hall"
    assert r.is_accessible is True
    assert r.is_clean is True
    assert r.maintenance_required is False
    assert r.cleaning_log == []
    assert r.access_log == []

def test_invalid_location():
    with pytest.raises(ValueError, match="Invalid restroom location: basement"):
        Restroom("basement", is_accessible=False)

@pytest.fixture
def restroom():
    return Restroom("gate area", is_accessible=False)

def test_mark_dirty(restroom):
    restroom.mark_dirty()
    assert restroom.is_clean is False

def test_clean(restroom):
    restroom.mark_dirty()
    restroom.mark_for_maintenance()
    restroom.clean("Olga")
    assert restroom.is_clean is True
    assert restroom.maintenance_required is False
    assert restroom.cleaning_log == ["Olga"]

def test_mark_and_clear_maintenance(restroom):
    restroom.mark_for_maintenance()
    assert restroom.maintenance_required is True
    restroom.clear_maintenance()
    assert restroom.maintenance_required is False

def test_log_access_and_count(restroom):
    restroom.log_access("user1")
    restroom.log_access("user2")
    assert restroom.access_log == ["user1", "user2"]
    assert restroom.access_count() == 2

def test_cleaning_count(restroom):
    restroom.clean("staff1")
    restroom.clean("staff2")
    assert restroom.cleaning_count() == 2

def test_is_operational(restroom):
    assert restroom.is_operational() is True
    restroom.mark_for_maintenance()
    assert restroom.is_operational() is False

def test_reset(restroom):
    restroom.mark_dirty()
    restroom.mark_for_maintenance()
    restroom.clean("A")
    restroom.log_access("B")
    restroom.reset()
    assert restroom.is_clean is True
    assert restroom.maintenance_required is False
    assert restroom.cleaning_log == []
    assert restroom.access_log == []

def test_summary_accessible():
    r = Restroom("vip lounge", is_accessible=True)
    assert r.summary() == "vip lounge restroom (accessible)"

def test_summary_standard():
    r = Restroom("main lobby", is_accessible=False)
    assert r.summary() == "main lobby restroom (standard)"
