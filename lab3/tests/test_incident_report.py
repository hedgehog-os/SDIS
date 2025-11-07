import pytest
from models.operations.incident_report import IncidentReport

def test_valid_initialization():
    report = IncidentReport("IR001", "Fire alarm triggered", "high", "2025-11-06T10:00")
    assert report.report_id == "IR001"
    assert report.description == "Fire alarm triggered"
    assert report.severity == "high"
    assert report.timestamp == "2025-11-06T10:00"
    assert report.is_resolved is False
    assert report.resolution_notes == []
    assert report.associated_zones == []
    assert report.reviewed is False

def test_invalid_severity_level():
    with pytest.raises(ValueError, match="Invalid severity level: extreme"):
        IncidentReport("IR002", "Unknown issue", "extreme", "2025-11-06T11:00")

@pytest.fixture
def report():
    return IncidentReport("IR003", "Security breach", "critical", "2025-11-06T12:00")

def test_resolve(report):
    report.resolve("Issue contained")
    assert report.is_resolved is True
    assert report.resolution_notes == ["Issue contained"]

def test_reopen(report):
    report.resolve("Initial fix")
    report.reopen("Reopened due to recurrence")
    assert report.is_resolved is False
    assert report.resolution_notes == ["Initial fix", "Reopened due to recurrence"]

def test_mark_reviewed(report):
    report.mark_reviewed()
    assert report.reviewed is True

def test_add_zone(report):
    report.add_zone("Zone A")
    report.add_zone("Zone B")
    report.add_zone("Zone A")  # duplicate
    assert report.associated_zones == ["Zone A", "Zone B"]

def test_remove_zone_success(report):
    report.add_zone("Zone X")
    assert report.remove_zone("Zone X") is True
    assert "Zone X" not in report.associated_zones

def test_remove_zone_failure(report):
    assert report.remove_zone("Unknown") is False

def test_get_zone_list(report):
    report.add_zone("Z1")
    report.add_zone("Z2")
    zones = report.get_zone_list()
    assert zones == ["Z1", "Z2"]
    assert zones is not report.associated_zones  # ensure it's a copy

def test_reset(report):
    report.resolve("Fixed")
    report.add_zone("Z1")
    report.mark_reviewed()
    report.reset()
    assert report.is_resolved is False
    assert report.resolution_notes == []
    assert report.associated_zones == []
    assert report.reviewed is False

def test_summary_open(report):
    report.add_zone("Z1")
    summary = report.summary()
    assert summary == "Incident IR003 [CRITICAL] at 2025-11-06T12:00: OPEN, Zones: 1, Reviewed: False"

def test_summary_resolved_reviewed(report):
    report.add_zone("Z1")
    report.resolve("Resolved")
    report.mark_reviewed()
    summary = report.summary()
    assert summary == "Incident IR003 [CRITICAL] at 2025-11-06T12:00: RESOLVED, Zones: 1, Reviewed: True"
