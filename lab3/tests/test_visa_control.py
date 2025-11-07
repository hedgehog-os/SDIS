import pytest
from models.operations.visa_control import VisaControl

class DummyVisa:
    def __init__(self, country, valid_dates):
        self.country = country
        self.valid_dates = valid_dates

    def is_valid(self, date):
        return date in self.valid_dates

class DummyPassenger:
    def __init__(self, full_name, visas=None):
        self.full_name = full_name
        self.visas = visas or []

@pytest.fixture
def control():
    vc = VisaControl("Germany")
    vc.verified_passengers = []
    vc.failed_passengers = []
    vc.audit_log = []
    return vc

def test_verify_success(control):
    visa = DummyVisa("Germany", ["2025-11-04"])
    passenger = DummyPassenger("Alice", [visa])
    assert control.verify(passenger) is True

def test_verify_failure(control):
    visa = DummyVisa("France", ["2025-11-04"])
    passenger = DummyPassenger("Bob", [visa])
    assert control.verify(passenger) is False

def test_has_been_verified(control):
    passenger = DummyPassenger("Charlie")
    control.verified_passengers.append("Charlie")
    assert control.has_been_verified(passenger) is True

def test_has_failed_verification(control):
    passenger = DummyPassenger("Dana")
    control.failed_passengers.append("Dana")
    assert control.has_failed_verification(passenger) is True

def test_reset(control):
    control.verified_passengers.append("Eve")
    control.failed_passengers.append("Frank")
    control.audit_log.append("Audit entry")
    control.reset()
    assert control.verified_passengers == []
    assert control.failed_passengers == []
    assert control.audit_log == []

def test_summary(control):
    control.verified_passengers.extend(["Alice", "Bob"])
    control.failed_passengers.append("Charlie")
    assert control.summary() == "VisaControl for Germany: 2 verified, 1 denied"

def test_get_audit_log(control):
    control.audit_log.append("Checked Alice")
    log = control.get_audit_log()
    assert log == ["Checked Alice"]
    assert log is not control.audit_log  # ensure it's a copy
