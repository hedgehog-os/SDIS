import pytest
from models.staff.SecurityOfficer import SecurityOfficer

class DummyPassport:
    def __init__(self, number):
        self.number = number

class DummyPassenger:
    def __init__(self, full_name, passport_number="P123"):
        self.full_name = full_name
        self.passport = DummyPassport(passport_number)

@pytest.fixture
def officer():
    return SecurityOfficer("Dmitry", "SEC-001")

def test_inspect_passenger(officer):
    p = DummyPassenger("Alice")
    msg = officer.inspect_passenger(p)
    assert msg == "Security check completed for Alice"
    assert "Alice" in officer.inspected_passengers
    assert officer.inspection_log[-1]["passport"] == "P123"
    assert "Inspected Alice" in officer.notes[-1]

def test_flag_passenger(officer):
    p = DummyPassenger("Bob")
    officer.flag_passenger(p, "Suspicious behavior")
    assert officer.flagged_passengers["Bob"] == "Suspicious behavior"
    assert "Flagged Bob: Suspicious behavior" in officer.notes[-1]

def test_is_flagged_true(officer):
    p = DummyPassenger("Charlie")
    officer.flag_passenger(p, "Missing documents")
    assert officer.is_flagged(p) is True

def test_is_flagged_false(officer):
    p = DummyPassenger("Dana")
    assert officer.is_flagged(p) is False

def test_get_flag_reason(officer):
    p = DummyPassenger("Eve")
    officer.flag_passenger(p, "Late arrival")
    assert officer.get_flag_reason(p) == "Late arrival"

def test_get_flag_reason_none(officer):
    p = DummyPassenger("Frank")
    assert officer.get_flag_reason(p) is None

def test_generate_flag_report_with_flags(officer):
    officer.flag_passenger(DummyPassenger("Alice"), "Suspicious")
    officer.flag_passenger(DummyPassenger("Bob"), "Missing papers")
    report = officer.generate_flag_report()
    assert "Flagged Passengers Report — Officer Dmitry" in report
    assert "• Alice: Suspicious" in report
    assert "• Bob: Missing papers" in report

def test_generate_flag_report_empty(officer):
    report = officer.generate_flag_report()
    assert report == "No flagged passengers for Officer Dmitry (ID: SEC-001)"

def test_archive_flags(officer):
    officer.flag_passenger(DummyPassenger("Alice"), "Suspicious")
    officer.archive_flags()
    assert officer.flag_archive[-1] == {"Alice": "Suspicious"}
    assert officer.flagged_passengers == {}
    assert "Archived 1 flagged passenger(s)" in officer.notes[-1]

def test_get_flag_archive(officer):
    officer.flag_passenger(DummyPassenger("Alice"), "Suspicious")
    officer.archive_flags()
    archive = officer.get_flag_archive()
    assert archive == [{"Alice": "Suspicious"}]

def test_reset_inspections(officer):
    officer.inspect_passenger(DummyPassenger("Alice"))
    officer.reset_inspections()
    assert officer.inspected_passengers == []
    assert officer.inspection_log == []
    assert "Reset 1 inspection(s) for new shift" in officer.notes[-1]

def test_summary(officer):
    officer.inspect_passenger(DummyPassenger("Alice"))
    officer.flag_passenger(DummyPassenger("Bob"), "Suspicious")
    officer.archive_flags()
    summary = officer.summary()
    assert "Dmitry — Badge: SEC-001" in summary
    assert "Inspections: 1" in summary
    assert "Flags: 0" in summary
    assert "Archived snapshots: 1" in summary

def test_to_dict(officer):
    officer.inspect_passenger(DummyPassenger("Alice"))
    officer.flag_passenger(DummyPassenger("Bob"), "Suspicious")
    officer.archive_flags()
    d = officer.to_dict()
    assert d["name"] == "Dmitry"
    assert d["badge_id"] == "SEC-001"
    assert "Alice" in d["inspected_passengers"]
    assert "Bob" in d["flag_archive"][0]
    assert d["notes"] is not officer.notes
