import pytest
from models.staff.CrewSchedule import CrewSchedule

class DummyFlight:
    def __init__(self, flight_number):
        self.flight_number = flight_number

class DummyPilot:
    def __init__(self, name):
        self.name = name

class DummyAttendant:
    def __init__(self, name, languages):
        self.name = name
        self.languages = languages

@pytest.fixture
def flight():
    return DummyFlight("SU123")

@pytest.fixture
def schedule(flight):
    return CrewSchedule(flight)

def test_assign_pilot(schedule):
    pilot = DummyPilot("Ivan")
    schedule.assign_pilot(pilot)
    assert schedule.pilots == [pilot]
    assert f"Pilot Ivan assigned to flight SU123" in schedule.notes

def test_assign_attendant(schedule):
    attendant = DummyAttendant("Olga", ["English", "Russian"])
    schedule.assign_attendant(attendant)
    assert schedule.attendants == [attendant]
    assert f"Attendant Olga assigned to flight SU123" in schedule.notes

def test_is_complete_false(schedule):
    assert schedule.is_complete() is False

def test_is_complete_true(schedule):
    schedule.assign_pilot(DummyPilot("Ivan"))
    schedule.assign_attendant(DummyAttendant("Olga", ["English"]))
    schedule.assign_attendant(DummyAttendant("Anna", ["French"]))
    assert schedule.is_complete() is True

def test_get_languages(schedule):
    schedule.assign_attendant(DummyAttendant("Olga", ["English", "Russian"]))
    schedule.assign_attendant(DummyAttendant("Anna", ["French"]))
    langs = schedule.get_languages()
    assert langs == {"English", "Russian", "French"}

def test_get_crew_names(schedule):
    schedule.assign_pilot(DummyPilot("Ivan"))
    schedule.assign_attendant(DummyAttendant("Olga", ["English"]))
    names = schedule.get_crew_names()
    assert names == {"pilots": ["Ivan"], "attendants": ["Olga"]}

def test_summary_incomplete(schedule):
    summary = schedule.summary()
    assert "Pilots: None" in summary
    assert "Attendants: None" in summary
    assert "Languages covered: None" in summary
    assert "Status: Incomplete" in summary

def test_summary_complete(schedule):
    schedule.assign_pilot(DummyPilot("Ivan"))
    schedule.assign_attendant(DummyAttendant("Olga", ["English"]))
    schedule.assign_attendant(DummyAttendant("Anna", ["French"]))
    summary = schedule.summary()
    assert "Pilots: Ivan" in summary
    assert "Attendants: Olga, Anna" in summary
    assert "Languages covered: English, French" in summary
    assert "Status: Complete" in summary

def test_to_dict(schedule):
    schedule.assign_pilot(DummyPilot("Ivan"))
    schedule.assign_attendant(DummyAttendant("Olga", ["English"]))
    schedule.assign_attendant(DummyAttendant("Anna", ["French"]))
    d = schedule.to_dict()
    assert d["flight_number"] == "SU123"
    assert d["pilots"] == ["Ivan"]
    assert d["attendants"] == ["Olga", "Anna"]
    assert d["languages"] == ["English", "French"]
    assert d["is_complete"] is True
    assert "Pilot Ivan assigned to flight SU123" in d["notes"]
