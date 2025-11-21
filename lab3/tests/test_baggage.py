import pytest
from models.passenger.Baggage import Baggage

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

def test_initialization():
    bag = Baggage("BG123", 23.5, False)
    assert bag.tag_number == "BG123"
    assert bag.weight_kg == 23.5
    assert bag.is_fragile is False
    assert bag.owner is None
    assert bag.notes == []
    assert bag.is_checked_in is False

def test_assign_owner():
    passenger = DummyPassenger("Alice")
    bag = Baggage("BG124", 20.0, False)
    bag.assign_owner(passenger)
    assert bag.owner == passenger
    assert "Assigned to Alice" in bag.notes

def test_exceeds_limit_true():
    bag = Baggage("BG125", 25.0, False)
    assert bag.exceeds_limit(23.0) is True

def test_exceeds_limit_false():
    bag = Baggage("BG126", 20.0, False)
    assert bag.exceeds_limit(23.0) is False

def test_mark_fragile():
    bag = Baggage("BG127", 15.0, False)
    bag.mark_fragile()
    assert bag.is_fragile is True
    assert "Marked as fragile" in bag.notes

def test_unmark_fragile():
    bag = Baggage("BG128", 15.0, True)
    bag.unmark_fragile()
    assert bag.is_fragile is False
    assert "Unmarked as fragile" in bag.notes

def test_check_in():
    bag = Baggage("BG129", 18.0, False)
    bag.check_in()
    assert bag.is_checked_in is True
    assert "Checked in" in bag.notes

def test_uncheck():
    bag = Baggage("BG130", 18.0, False)
    bag.check_in()
    bag.uncheck()
    assert bag.is_checked_in is False
    assert "Unchecked" in bag.notes

def test_add_note():
    bag = Baggage("BG131", 22.0, False)
    bag.add_note("Handle with care")
    assert "Handle with care" in bag.notes

def test_summary_unassigned():
    bag = Baggage("BG132", 22.0, True)
    summary = bag.summary()
    assert summary == "Baggage BG132: 22.0 kg, Fragile, Pending, Owner: Unassigned"

def test_summary_checked_in_with_owner():
    passenger = DummyPassenger("Bob")
    bag = Baggage("BG133", 22.0, False)
    bag.assign_owner(passenger)
    bag.check_in()
    summary = bag.summary()
    assert summary == "Baggage BG133: 22.0 kg, Standard, Checked-in, Owner: Bob"
