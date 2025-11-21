import pytest
from models.staff.CleaningCrew import CleaningCrew

class DummyRestroom:
    def __init__(self, location_id):
        self.location_id = location_id
        self.cleaned = False

    def clean(self):
        self.cleaned = True

class DummyLounge:
    def __init__(self, name):
        self.name = name
        self.is_clean = False

@pytest.fixture
def crew():
    return CleaningCrew("CR-01", "Morning")

def test_clean_restroom(crew):
    r = DummyRestroom("R101")
    crew.clean_restroom(r)
    assert r.cleaned is True
    assert "R101" in crew.cleaned_restrooms
    assert "Cleaned restroom R101" in crew.notes

def test_clean_lounge(crew):
    l = DummyLounge("VIP Lounge")
    crew.clean_lounge(l)
    assert l.is_clean is True
    assert "VIP Lounge" in crew.cleaned_lounges
    assert "Cleaned lounge VIP Lounge" in crew.notes

def test_total_cleaned(crew):
    crew.cleaned_restrooms = ["R1", "R2"]
    crew.cleaned_lounges = ["L1"]
    assert crew.total_cleaned() == 3

def test_summary(crew):
    crew.cleaned_restrooms = ["R1"]
    crew.cleaned_lounges = ["L1", "L2"]
    summary = crew.summary()
    assert "Crew CR-01 (Shift: Morning)" in summary
    assert "- Restrooms cleaned: 1" in summary
    assert "- Lounges cleaned: 2" in summary
    assert "- Total tasks: 3" in summary

def test_to_dict(crew):
    crew.cleaned_restrooms = ["R1"]
    crew.cleaned_lounges = ["L1"]
    crew.notes = ["Note A"]
    d = crew.to_dict()
    assert d["crew_id"] == "CR-01"
    assert d["shift"] == "Morning"
    assert d["restrooms_cleaned"] == ["R1"]
    assert d["lounges_cleaned"] == ["L1"]
    assert d["notes"] == ["Note A"]
    assert d["notes"] is not crew.notes  # ensure it's a copy

def test_generate_cleaning_report_full(crew):
    crew.cleaned_restrooms = ["R1", "R2"]
    crew.cleaned_lounges = ["L1"]
    report = crew.generate_cleaning_report()
    assert "Restrooms cleaned (2):" in report
    assert "• Restroom R1" in report
    assert "• Restroom R2" in report
    assert "Lounges cleaned (1):" in report
    assert "• Lounge L1" in report

def test_generate_cleaning_report_empty(crew):
    report = crew.generate_cleaning_report()
    assert "No cleaning tasks recorded." in report

def test_reset_tasks(crew):
    crew.cleaned_restrooms = ["R1", "R2"]
    crew.cleaned_lounges = ["L1"]
    crew.reset_tasks()
    assert crew.cleaned_restrooms == []
    assert crew.cleaned_lounges == []
    assert "Reset tasks: 2 restroom(s), 1 lounge(s) cleared for new shift." in crew.notes[-1]
