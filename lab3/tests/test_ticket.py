import pytest
from models.passenger.Ticket import Ticket
from exceptions.TicketAlreadyCheckedInException import TicketAlreadyCheckedInException

class DummyFlight:
    def __init__(self, flight_id="FL001"):
        self.flight_id = flight_id

class DummyLoyaltyProgram:
    def __init__(self, tier="Basic", points=0):
        self.tier = tier
        self.points = points

class DummyPassenger:
    def __init__(self, full_name, loyalty_program=None):
        self.full_name = full_name
        self.loyalty_program = loyalty_program

@pytest.fixture
def ticket():
    return Ticket("T001", DummyFlight(), "12A", 100.0)

def test_apply_discount_no_passenger(ticket):
    ticket.apply_discount()
    assert ticket.price == 100.0
    assert ticket.notes == []

def test_apply_discount_no_loyalty(ticket):
    ticket.assign_passenger(DummyPassenger("Alice"))
    ticket.apply_discount()
    assert ticket.price == 100.0
    assert len(ticket.notes) == 1  # only "Assigned to Alice"

def test_apply_discount_basic_tier():
    passenger = DummyPassenger("Bob", DummyLoyaltyProgram("Basic", 500))
    ticket = Ticket("T002", DummyFlight(), "14B", 200.0)
    ticket.assign_passenger(passenger)
    ticket.apply_discount()
    assert ticket.price == 200.0
    assert "Basic discount applied" not in "".join(ticket.notes)

def test_apply_discount_silver_tier():
    passenger = DummyPassenger("Carol", DummyLoyaltyProgram("Silver", 500))
    ticket = Ticket("T003", DummyFlight(), "15C", 200.0)
    ticket.assign_passenger(passenger)
    ticket.apply_discount()
    assert round(ticket.price, 2) == 190.0
    assert "Silver discount applied" in ticket.notes[-1]

def test_apply_discount_gold_tier():
    passenger = DummyPassenger("Dave", DummyLoyaltyProgram("Gold", 500))
    ticket = Ticket("T004", DummyFlight(), "16D", 200.0)
    ticket.assign_passenger(passenger)
    ticket.apply_discount()
    assert round(ticket.price, 2) == 180.0
    assert "Gold discount applied" in ticket.notes[-1]

def test_apply_discount_platinum_tier():
    passenger = DummyPassenger("Eve", DummyLoyaltyProgram("Platinum", 500))
    ticket = Ticket("T005", DummyFlight(), "17E", 200.0)
    ticket.assign_passenger(passenger)
    ticket.apply_discount()
    assert round(ticket.price, 2) == 170.0
    assert "Platinum discount applied" in ticket.notes[-1]

def test_is_upgrade_eligible_true():
    passenger = DummyPassenger("Frank", DummyLoyaltyProgram(points=1500))
    ticket = Ticket("T006", DummyFlight(), "18F", 200.0)
    ticket.assign_passenger(passenger)
    assert ticket.is_upgrade_eligible() is True

def test_is_upgrade_eligible_false_no_passenger():
    ticket = Ticket("T007", DummyFlight(), "19G", 200.0)
    assert ticket.is_upgrade_eligible() is False

def test_is_upgrade_eligible_false_no_loyalty():
    passenger = DummyPassenger("Grace")
    ticket = Ticket("T008", DummyFlight(), "20H", 200.0)
    ticket.assign_passenger(passenger)
    assert ticket.is_upgrade_eligible() is False

def test_is_upgrade_eligible_false_low_points():
    passenger = DummyPassenger("Heidi", DummyLoyaltyProgram(points=500))
    ticket = Ticket("T009", DummyFlight(), "21J", 200.0)
    ticket.assign_passenger(passenger)
    assert ticket.is_upgrade_eligible() is False

def test_check_in_then_uncheck_then_check_in_again():
    ticket = Ticket("T013", DummyFlight(), "25A", 180.0)
    ticket.check_in()
    ticket.uncheck()
    assert ticket.is_checked_in is False
    ticket.check_in()
    assert ticket.is_checked_in is True
    assert ticket.notes[-1] == "Checked in"

def test_to_dict_unassigned_passenger():
    ticket = Ticket("T014", DummyFlight(), "26B", 180.0)
    d = ticket.to_dict()
    assert d["passenger_name"] is None
    assert d["notes"] == []

def test_summary_with_price_formatting():
    ticket = Ticket("T015", DummyFlight(), "27C", 199.999)
    summary = ticket.summary()
    assert "$200.00" in summary  # rounded formatting

def test_check_in_exception_message():
    ticket = Ticket("T016", DummyFlight(), "28D", 180.0)
    ticket.check_in()
    with pytest.raises(TicketAlreadyCheckedInException) as exc:
        ticket.check_in()
    assert ticket.ticket_id in str(exc.value)

def test_apply_discount_unknown_tier():
    class WeirdLoyalty:
        def __init__(self):
            self.tier = "Diamond"
            self.points = 9999
    passenger = DummyPassenger("Zoe", WeirdLoyalty())
    ticket = Ticket("T017", DummyFlight(), "29E", 300.0)
    ticket.assign_passenger(passenger)
    ticket.apply_discount()
    assert ticket.price == 300.0
    assert not any("Diamond" in note for note in ticket.notes)
