class FlightOverbookedException(Exception):
    def __init__(self, flight_number: str) -> None:
        super().__init__(f"Flight {flight_number} is overbooked. Cannot board more passengers.")

