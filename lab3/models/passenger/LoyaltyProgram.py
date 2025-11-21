from __future__ import annotations
from typing import Optional

class LoyaltyProgram:
    VALID_TIERS = ["Basic", "Silver", "Gold", "Platinum"]

    def __init__(self, program_name: str, member_id: str, tier: str, points: int = 0) -> None:
        if tier not in self.VALID_TIERS:
            raise ValueError(f"Invalid tier: {tier}")
        self.program_name: str = program_name
        self.member_id: str = member_id
        self.tier: str = tier
        self.points: int = points
        self.history: list[str] = []
        self.owner_name: Optional[str] = None

    def add_points(self, amount: int, reason: str = "Activity") -> None:
        self.points += amount
        self.history.append(f"+{amount} points for {reason}")

    def redeem_points(self, amount: int, reason: str = "Redemption") -> bool:
        if amount > self.points:
            self.history.append(f"Failed redemption: {amount} points for {reason}")
            return False
        self.points -= amount
        self.history.append(f"-{amount} points for {reason}")
        return True

    def upgrade_tier(self, new_tier: str) -> None:
        if new_tier not in self.VALID_TIERS:
            raise ValueError(f"Invalid tier: {new_tier}")
        self.tier = new_tier
        self.history.append(f"Tier upgraded to {new_tier}")

    def assign_owner(self, full_name: str) -> None:
        self.owner_name = full_name
        self.history.append(f"Assigned to {full_name}")

    def summary(self) -> str:
        return (
            f"{self.program_name} member {self.member_id} ({self.tier}) — "
            f"{self.points} points, Owner: {self.owner_name or 'Unassigned'}"
        )

    def get_history(self) -> list[str]:
        return self.history.copy()
