class FlightCapacityExceededException(Exception):
    def __init__(self, flight_number: str) -> None:
        super().__init__(f"Flight {flight_number} is at full capacity")

