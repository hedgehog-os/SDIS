import pytest
from models.staff.CustomsOfficer import CustomsOfficer

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

@pytest.fixture
def officer():
    return CustomsOfficer("Ivan", "CO-001")

def test_inspect_passenger(officer):
    p = DummyPassenger("Alice")
    msg = officer.inspect_passenger(p)
    assert msg == "Customs inspection completed for Alice"
    assert "Alice" in officer.inspected_passengers
    assert "Inspected Alice" in officer.notes

def test_flag_passenger(officer):
    p = DummyPassenger("Bob")
    officer.flag_passenger(p, "Suspicious behavior")
    assert officer.flagged_passengers["Bob"] == "Suspicious behavior"
    assert "Flagged Bob: Suspicious behavior" in officer.notes

def test_has_inspected_true(officer):
    p = DummyPassenger("Charlie")
    officer.inspect_passenger(p)
    assert officer.has_inspected(p) is True

def test_has_inspected_false(officer):
    p = DummyPassenger("Dana")
    assert officer.has_inspected(p) is False

def test_is_flagged_true(officer):
    p = DummyPassenger("Eve")
    officer.flag_passenger(p, "Missing documents")
    assert officer.is_flagged(p) is True

def test_is_flagged_false(officer):
    p = DummyPassenger("Frank")
    assert officer.is_flagged(p) is False

def test_summary(officer):
    officer.inspect_passenger(DummyPassenger("Alice"))
    officer.flag_passenger(DummyPassenger("Bob"), "Suspicious")
    summary = officer.summary()
    assert "Officer Ivan (ID: CO-001)" in summary
    assert "- Total inspections: 1" in summary
    assert "- Flagged passengers: 1" in summary

def test_to_dict(officer):
    officer.inspect_passenger(DummyPassenger("Alice"))
    officer.flag_passenger(DummyPassenger("Bob"), "Suspicious")
    d = officer.to_dict()
    assert d["name"] == "Ivan"
    assert d["officer_id"] == "CO-001"
    assert d["inspected_passengers"] == ["Alice"]
    assert d["flagged_passengers"] == {"Bob": "Suspicious"}
    assert "Inspected Alice" in d["notes"]
    assert "Flagged Bob: Suspicious" in d["notes"]
    assert d["notes"] is not officer.notes  # ensure it's a copy

def test_generate_flag_report_with_flags(officer):
    officer.flag_passenger(DummyPassenger("Alice"), "Suspicious")
    officer.flag_passenger(DummyPassenger("Bob"), "Missing papers")
    report = officer.generate_flag_report()
    assert "Flagged Passengers Report" in report
    assert "• Alice: Suspicious" in report
    assert "• Bob: Missing papers" in report

def test_generate_flag_report_empty(officer):
    report = officer.generate_flag_report()
    assert report == "No flagged passengers for Officer Ivan (ID: CO-001)"

def test_reset_flags(officer):
    officer.flag_passenger(DummyPassenger("Alice"), "Suspicious")
    officer.reset_flags()
    assert officer.flagged_passengers == {}
    assert "Reset 1 flagged passenger(s) for new shift." in officer.notes

def test_archive_flags(officer):
    officer.flag_passenger(DummyPassenger("Alice"), "Suspicious")
    snapshot = officer.archive_flags()
    assert snapshot == {"Alice": "Suspicious"}
    assert officer.flag_archive[-1] == snapshot
    assert "Archived 1 flagged passenger(s)" in officer.notes

def test_get_flag_archive_empty(officer):
    archive = officer.get_flag_archive()
    assert archive == []

def test_get_flag_archive_after_archive(officer):
    officer.flag_passenger(DummyPassenger("Alice"), "Suspicious")
    officer.archive_flags()
    archive = officer.get_flag_archive()
    assert archive == [{"Alice": "Suspicious"}]
