import pytest
from models.passenger.LoyaltyProgram import LoyaltyProgram

def test_valid_initialization():
    lp = LoyaltyProgram("SkyClub", "SC123", "Gold", 500)
    assert lp.program_name == "SkyClub"
    assert lp.member_id == "SC123"
    assert lp.tier == "Gold"
    assert lp.points == 500
    assert lp.owner_name is None
    assert lp.history == []

def test_invalid_tier():
    with pytest.raises(ValueError, match="Invalid tier: Diamond"):
        LoyaltyProgram("SkyClub", "SC124", "Diamond")

@pytest.fixture
def loyalty():
    return LoyaltyProgram("SkyClub", "SC125", "Silver", 1000)

def test_add_points(loyalty):
    loyalty.add_points(200, "Flight bonus")
    assert loyalty.points == 1200
    assert loyalty.history[-1] == "+200 points for Flight bonus"

def test_redeem_points_success(loyalty):
    result = loyalty.redeem_points(300, "Upgrade")
    assert result is True
    assert loyalty.points == 700
    assert loyalty.history[-1] == "-300 points for Upgrade"

def test_redeem_points_failure(loyalty):
    result = loyalty.redeem_points(2000, "Lounge access")
    assert result is False
    assert loyalty.points == 1000
    assert loyalty.history[-1] == "Failed redemption: 2000 points for Lounge access"

def test_upgrade_tier(loyalty):
    loyalty.upgrade_tier("Gold")
    assert loyalty.tier == "Gold"
    assert loyalty.history[-1] == "Tier upgraded to Gold"

def test_upgrade_invalid_tier(loyalty):
    with pytest.raises(ValueError, match="Invalid tier: Elite"):
        loyalty.upgrade_tier("Elite")

def test_assign_owner(loyalty):
    loyalty.assign_owner("Alice")
    assert loyalty.owner_name == "Alice"
    assert loyalty.history[-1] == "Assigned to Alice"

def test_summary_unassigned():
    lp = LoyaltyProgram("SkyClub", "SC126", "Basic")
    assert lp.summary() == "SkyClub member SC126 (Basic) — 0 points, Owner: Unassigned"

def test_summary_assigned(loyalty):
    loyalty.assign_owner("Bob")
    assert loyalty.summary() == "SkyClub member SC125 (Silver) — 1000 points, Owner: Bob"

def test_get_history_copy(loyalty):
    loyalty.add_points(100)
    history = loyalty.get_history()
    assert history == loyalty.history
    assert history is not loyalty.history  # ensure it's a copy
