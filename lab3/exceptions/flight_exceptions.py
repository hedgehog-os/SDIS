class FlightOverbookedException(Exception):
    def __init__(self, flight_number: str) -> None:
        super().__init__(f"Flight {flight_number} is overbooked. Cannot board more passengers.")

class GateConflictException(Exception):
    def __init__(self, gate_number: str) -> None:
        super().__init__(f"Gate {gate_number} is already assigned to another flight.")

class FlightCapacityExceededException(Exception):
    def __init__(self, flight_number: str) -> None:
        super().__init__(f"Flight {flight_number} is at full capacity")
