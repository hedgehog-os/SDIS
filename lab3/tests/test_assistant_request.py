import pytest
from models.passenger.assistance_request import SpecialAssistanceRequest

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

def test_valid_initialization():
    p = DummyPassenger("Alice")
    req = SpecialAssistanceRequest(p, "wheelchair", "Needs help boarding")
    assert req.passenger == p
    assert req.request_type == "wheelchair"
    assert req.description == "Needs help boarding"
    assert req.is_confirmed is False
    assert req.assigned_staff is None
    assert req.notes == []

def test_invalid_request_type():
    p = DummyPassenger("Bob")
    with pytest.raises(ValueError, match="Invalid request type: teleportation"):
        SpecialAssistanceRequest(p, "teleportation", "Sci-fi request")

@pytest.fixture
def assistance_request():
    return SpecialAssistanceRequest(DummyPassenger("Charlie"), "visual aid", "Needs help reading signs")

def test_confirm(assistance_request):
    assistance_request.confirm()
    assert assistance_request.is_confirmed is True

def test_cancel(assistance_request):
    assistance_request.confirm()
    assistance_request.cancel("Changed mind")
    assert assistance_request.is_confirmed is False
    assert assistance_request.notes == ["Cancelled: Changed mind"]

def test_assign_staff(assistance_request):
    assistance_request.assign_staff("Olga")
    assert assistance_request.assigned_staff == "Olga"
    assert "Assigned to Olga" in assistance_request.notes

def test_unassign_staff(assistance_request):
    assistance_request.assign_staff("Ivan")
    assistance_request.unassign_staff()
    assert assistance_request.assigned_staff is None
    assert "Unassigned from Ivan" in assistance_request.notes

def test_add_note(assistance_request):
    assistance_request.add_note("Passenger prefers morning slot")
    assert assistance_request.notes == ["Passenger prefers morning slot"]

def test_reset(assistance_request):
    assistance_request.confirm()
    assistance_request.assign_staff("Nikolai")
    assistance_request.add_note("Initial setup")
    assistance_request.reset()
    assert assistance_request.is_confirmed is False
    assert assistance_request.assigned_staff is None
    assert assistance_request.notes == []

def test_summary_pending(assistance_request):
    summary = assistance_request.summary()
    assert summary == (
        "Assistance for Charlie [visual aid] — PENDING. Description: Needs help reading signs"
    )

def test_summary_confirmed_with_staff(assistance_request):
    assistance_request.confirm()
    assistance_request.assign_staff("Olga")
    summary = assistance_request.summary()
    assert summary == (
        "Assistance for Charlie [visual aid] — CONFIRMED, Staff: Olga. Description: Needs help reading signs"
    )
