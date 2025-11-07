import pytest
from models.operations.lost_and_found_report import LostAndFoundReport

class DummyRestroom:
    def __init__(self, location):
        self.location = location

@pytest.fixture
def report():
    restroom = DummyRestroom("Main Lobby")
    return LostAndFoundReport("Black wallet", restroom.location, "2025-11-06T10:00")

def test_initialization(report):
    assert report.item_description == "Black wallet"
    assert report.location == "main lobby"
    assert report.timestamp == "2025-11-06T10:00"
    assert report.is_claimed is False
    assert report.claimed_by is None
    assert report.notes == []

def test_claim(report):
    report.claim("Alice")
    assert report.is_claimed is True
    assert report.claimed_by == "Alice"

def test_unclaim(report):
    report.claim("Bob")
    report.unclaim()
    assert report.is_claimed is False
    assert report.claimed_by is None

def test_add_note(report):
    report.add_note("Found near sink")
    report.add_note("Reported by cleaner")
    assert report.notes == ["Found near sink", "Reported by cleaner"]

def test_reset(report):
    report.claim("Charlie")
    report.add_note("Initial claim")
    report.reset()
    assert report.is_claimed is False
    assert report.claimed_by is None
    assert report.notes == []

def test_summary_unclaimed(report):
    summary = report.summary()
    assert summary == "Item: 'Black wallet' at main lobby on 2025-11-06T10:00 — UNCLAIMED"

def test_summary_claimed(report):
    report.claim("Dana")
    summary = report.summary()
    assert summary == "Item: 'Black wallet' at main lobby on 2025-11-06T10:00 — CLAIMED by Dana"
