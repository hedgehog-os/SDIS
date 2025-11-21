class GateConflictException(Exception):
    def __init__(self, gate_number: str) -> None:
        super().__init__(f"Gate {gate_number} is already assigned to another flight.")

