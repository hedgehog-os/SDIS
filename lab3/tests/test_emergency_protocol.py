import pytest
from models.operations.EmergencyProtocol import EmergencyProtocol

def test_valid_initialization():
    ep = EmergencyProtocol("EP001", "Fire in terminal", "high")
    assert ep.protocol_id == "EP001"
    assert ep.description == "Fire in terminal"
    assert ep.severity_level == "high"
    assert ep.is_active is False
    assert ep.activation_log == []
    assert ep.deactivation_log == []
    assert ep.associated_zones == []
    assert ep.reviewed is False

def test_invalid_severity_level():
    with pytest.raises(ValueError, match="Invalid severity level: extreme"):
        EmergencyProtocol("EP002", "Unknown threat", "extreme")

@pytest.fixture
def protocol():
    return EmergencyProtocol("EP003", "Security breach", "critical")

def test_activate(protocol):
    protocol.activate("2025-11-06T10:00")
    assert protocol.is_active is True
    assert protocol.activation_log == ["2025-11-06T10:00"]

def test_deactivate(protocol):
    protocol.activate("T1")
    protocol.deactivate("T2")
    assert protocol.is_active is False
    assert protocol.deactivation_log == ["T2"]

def test_mark_reviewed(protocol):
    protocol.mark_reviewed()
    assert protocol.reviewed is True

def test_reset(protocol):
    protocol.activate("T1")
    protocol.deactivate("T2")
    protocol.add_zone("Gate A")
    protocol.mark_reviewed()
    protocol.reset()
    assert protocol.is_active is False
    assert protocol.activation_log == []
    assert protocol.deactivation_log == []
    assert protocol.associated_zones == []
    assert protocol.reviewed is False

def test_add_zone(protocol):
    protocol.add_zone("Zone 1")
    protocol.add_zone("Zone 2")
    protocol.add_zone("Zone 1")  # duplicate
    assert protocol.associated_zones == ["Zone 1", "Zone 2"]

def test_remove_zone_success(protocol):
    protocol.add_zone("Zone X")
    assert protocol.remove_zone("Zone X") is True
    assert "Zone X" not in protocol.associated_zones

def test_remove_zone_failure(protocol):
    assert protocol.remove_zone("Unknown") is False

def test_get_zone_list(protocol):
    protocol.add_zone("Z1")
    protocol.add_zone("Z2")
    zones = protocol.get_zone_list()
    assert zones == ["Z1", "Z2"]
    assert zones is not protocol.associated_zones  # ensure it's a copy

def test_summary_active(protocol):
    protocol.add_zone("Z1")
    protocol.activate("T1")
    summary = protocol.summary()
    assert summary == "Protocol EP003 [CRITICAL]: ACTIVE, Zones: 1, Reviewed: False"

def test_summary_inactive_reviewed(protocol):
    protocol.add_zone("Z1")
    protocol.mark_reviewed()
    summary = protocol.summary()
    assert summary == "Protocol EP003 [CRITICAL]: INACTIVE, Zones: 1, Reviewed: True"
