import pytest
from models.staff.baggage_handler import BaggageHandler

class DummyOwner:
    def __init__(self, full_name):
        self.full_name = full_name

class DummyBaggage:
    def __init__(self, tag_number, weight_kg, is_fragile=False, owner=None):
        self.tag_number = tag_number
        self.weight_kg = weight_kg
        self.is_fragile = is_fragile
        self.owner = owner
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

@pytest.fixture
def handler():
    return BaggageHandler("Sergey", "Night")

def test_load_baggage(handler):
    b = DummyBaggage("BG001", 20.0)
    handler.load_baggage(b)
    assert b in handler.handled_baggage
    assert "Loaded baggage BG001" in handler.notes

def test_unload_baggage(handler):
    b = DummyBaggage("BG002", 22.0)
    handler.load_baggage(b)
    handler.unload_baggage(b)
    assert b not in handler.handled_baggage
    assert "Unloaded baggage BG002" in handler.notes

def test_total_weight(handler):
    handler.load_baggage(DummyBaggage("BG003", 10.0))
    handler.load_baggage(DummyBaggage("BG004", 15.5))
    assert handler.total_weight() == 25.5

def test_fragile_items(handler):
    b1 = DummyBaggage("BG005", 10.0, is_fragile=True)
    b2 = DummyBaggage("BG006", 12.0, is_fragile=False)
    handler.load_baggage(b1)
    handler.load_baggage(b2)
    fragile = handler.fragile_items()
    assert fragile == [b1]

def test_baggage_by_owner(handler):
    owner = DummyOwner("Alice")
    b1 = DummyBaggage("BG007", 10.0, owner=owner)
    b2 = DummyBaggage("BG008", 12.0)
    handler.load_baggage(b1)
    handler.load_baggage(b2)
    result = handler.baggage_by_owner("Alice")
    assert result == [b1]

def test_summary(handler):
    handler.load_baggage(DummyBaggage("BG009", 10.0))
    summary = handler.summary()
    assert "Handler: Sergey" in summary
    assert "Handled baggage: 1 items" in summary

def test_to_dict(handler):
    b = DummyBaggage("BG010", 10.0)
    handler.load_baggage(b)
    d = handler.to_dict()
    assert d["name"] == "Sergey"
    assert d["shift"] == "Night"
    assert d["handled_baggage_tags"] == ["BG010"]
    assert d["notes"] == handler.notes
    assert d["notes"] is not handler.notes  # ensure it's a copy

def test_flag_overweight_items(handler):
    b1 = DummyBaggage("BG011", 24.0)
    b2 = DummyBaggage("BG012", 22.0)
    handler.load_baggage(b1)
    handler.load_baggage(b2)
    flagged = handler.flag_overweight_items(23.0)
    assert flagged == ["BG011 — 24.0 kg"]
    assert "Flagged overweight baggage BG011" in handler.notes[-1]

def test_generate_report(handler):
    b1 = DummyBaggage("BG013", 24.0, is_fragile=True)
    b2 = DummyBaggage("BG014", 22.0)
    handler.load_baggage(b1)
    handler.load_baggage(b2)
    report = handler.generate_report()
    assert "- Total baggage handled: 2" in report
    assert "- Fragile items: 1" in report
    assert "- Overweight items (>23kg): 1" in report

def test_assign_to_flight(handler):
    b1 = DummyBaggage("BG015", 10.0)
    b2 = DummyBaggage("BG016", 12.0)
    handler.load_baggage(b1)
    handler.load_baggage(b2)
    handler.assign_to_flight("FL123")
    assert "Assigned to flight FL123" in b1.notes
    assert "Assigned to flight FL123" in b2.notes
    assert "All baggage assigned to flight FL123" in handler.notes

def test_group_by_owner(handler):
    owner1 = DummyOwner("Alice")
    owner2 = DummyOwner("Bob")
    b1 = DummyBaggage("BG017", 10.0, owner=owner1)
    b2 = DummyBaggage("BG018", 12.0, owner=owner2)
    b3 = DummyBaggage("BG019", 15.0)
    handler.load_baggage(b1)
    handler.load_baggage(b2)
    handler.load_baggage(b3)
    grouped = handler.group_by_owner()
    assert grouped == {
        "Alice": ["BG017"],
        "Bob": ["BG018"],
        "Unassigned": ["BG019"]
    }

def test_generate_manifest(handler):
    owner = DummyOwner("Charlie")
    b1 = DummyBaggage("BG020", 10.0, owner=owner)
    b2 = DummyBaggage("BG021", 12.0)
    handler.load_baggage(b1)
    handler.load_baggage(b2)
    manifest = handler.generate_manifest()
    assert "Manifest for Sergey" in manifest
    assert "- Charlie: 1 item(s)" in manifest
    assert "- Unassigned: 1 item(s)" in manifest
    assert "• BG020" in manifest
    assert "• BG021" in manifest
