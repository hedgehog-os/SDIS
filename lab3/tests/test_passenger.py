import pytest
from models.passenger.passenger import Passenger
from exceptions import InvalidPassportException

class DummyPassport:
    def __init__(self, number, valid_dates):
        self.number = number
        self.valid_dates = valid_dates

    def is_valid(self, date):
        return date in self.valid_dates

class DummyTicket:
    def __init__(self, code):
        self.code = code

class DummyVisa:
    def __init__(self, country, visa_type, expiration_date, valid_dates):
        self.country = country
        self.visa_type = visa_type
        self.expiration_date = expiration_date
        self.valid_dates = valid_dates

    def is_valid(self, date):
        return date in self.valid_dates

    def get_expiry_status(self, date):
        return "Valid" if self.is_valid(date) else "Expired"

class DummyBaggage:
    def __init__(self, tag_number, weight_kg):
        self.tag_number = tag_number
        self.weight_kg = weight_kg

class DummyLoyaltyProgram:
    def __init__(self, tier="Silver", points=1000):
        self.tier = tier
        self.points = points
        self.history = []
        self.owner_name = None

    def assign_owner(self, name):
        self.owner_name = name
        self.history.append(f"Assigned to {name}")

    def add_points(self, amount, reason):
        self.points += amount
        self.history.append(f"+{amount} points for {reason}")

    def redeem_points(self, amount, reason):
        if amount > self.points:
            self.history.append(f"Failed redemption: {amount} points for {reason}")
            return False
        self.points -= amount
        self.history.append(f"-{amount} points for {reason}")
        return True

@pytest.fixture
def passenger():
    passport = DummyPassport("P123", ["2025-11-06"])
    ticket = DummyTicket("T456")
    return Passenger("Alice", passport, ticket)

def test_add_baggage(passenger):
    b1 = DummyBaggage("B1", 10.0)
    b2 = DummyBaggage("B2", 15.0)
    passenger.add_baggage(b1)
    passenger.add_baggage(b2)
    assert passenger.total_baggage_weight() == 25.0
    assert passenger.overweight_baggage(12.0) == [b2]

def test_validate_passport_valid(passenger):
    passenger.validate_passport("2025-11-06")  # no exception

def test_validate_passport_invalid():
    passport = DummyPassport("P999", [])
    ticket = DummyTicket("T999")
    p = Passenger("Bob", passport, ticket)
    with pytest.raises(InvalidPassportException):
        p.validate_passport("2025-11-06")

def test_visa_management(passenger):
    visa1 = DummyVisa("Germany", "Tourist", "2025-12-01", ["2025-11-06"])
    visa2 = DummyVisa("France", "Business", "2025-10-01", [])
    passenger.add_visa(visa1)
    passenger.add_visa(visa2)
    assert passenger.has_valid_visa_for("Germany", "2025-11-06") is True
    assert passenger.has_valid_visa_for("France", "2025-11-06") is False
    assert passenger.get_valid_visas("2025-11-06") == [visa1]
    assert passenger.get_expired_visas("2025-11-06") == [visa2]
    assert passenger.get_visa_for_country("Germany") == visa1

def test_loyalty_program(passenger):
    lp = DummyLoyaltyProgram()
    passenger.enroll_loyalty_program(lp)
    assert passenger.get_loyalty_status() == "Silver — 1000 points"
    passenger.add_loyalty_points(500)
    assert passenger.loyalty_program.points == 1500
    assert passenger.redeem_loyalty_points(200) is True
    assert passenger.redeem_loyalty_points(5000) is False

def test_boarding_checks(passenger):
    visa = DummyVisa("Germany", "Tourist", "2025-12-01", ["2025-11-06"])
    passenger.add_visa(visa)
    passenger.add_baggage(DummyBaggage("B1", 10.0))
    assert passenger.is_ready_for_boarding("Germany", "2025-11-06", 20.0) is True
    assert passenger.boarding_issues("Germany", "2025-11-06", 20.0) == []
    assert "cleared for boarding" in passenger.auto_notify("Germany", "2025-11-06", 20.0)

def test_boarding_issues(passenger):
    passenger.passport.valid_dates = []  # invalidate passport
    passenger.add_baggage(DummyBaggage("B1", 25.0))
    issues = passenger.boarding_issues("France", "2025-11-06", 20.0)
    assert "Passport is invalid" in issues[0]
    assert "No valid visa" in issues[1]
    assert "Baggage exceeds limit" in issues[2]

def test_check_in_summary(passenger):
    passenger.add_visa(DummyVisa("Germany", "Tourist", "2025-12-01", ["2025-11-06"]))
    passenger.add_baggage(DummyBaggage("B1", 10.0))
    summary = passenger.check_in_summary("Germany", "2025-11-06", 20.0)
    assert "Ready for boarding: Yes" in summary

def test_summary(passenger):
    passenger.add_baggage(DummyBaggage("B1", 10.0))
    passenger.add_visa(DummyVisa("Germany", "Tourist", "2025-12-01", ["2025-11-06"]))
    assert "Baggage: 1 items" in passenger.summary()

def test_visa_summary(passenger):
    passenger.add_visa(DummyVisa("Germany", "Tourist", "2025-12-01", ["2025-11-06"]))
    passenger.add_visa(DummyVisa("France", "Business", "2025-10-01", []))
    summary = passenger.get_visa_summary("2025-11-06")
    assert "- Germany (Tourist)" in summary
    assert "- France (Business)" in summary

def test_remove_expired_visas(capfd, passenger):
    passenger.add_visa(DummyVisa("Germany", "Tourist", "2025-12-01", ["2025-11-06"]))
    passenger.add_visa(DummyVisa("France", "Business", "2025-10-01", []))
    passenger.remove_expired_visas("2025-11-06")
    out, _ = capfd.readouterr()
    assert "1 expired visa(s) removed" in out

def test_to_dict(passenger):
    passenger.notes.append("Late check-in")
    passenger.add_baggage(DummyBaggage("B1", 10.0))
    passenger.add_visa(DummyVisa("Germany", "Tourist", "2025-12-01", ["2025-11-06"]))
    d = passenger.to_dict()
    assert d["full_name"] == "Alice"
    assert d["passport_number"] == "P123"
    assert d["ticket_code"] == "T456"
    assert d["baggage_tags"] == ["B1"]
    assert d["total_baggage_weight"] == 10.0
    assert d["valid_visas"] == ["Germany"]
    assert d["notes"] == ["Late check-in"]
