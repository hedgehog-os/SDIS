class UnauthorizedAircraftAccessException(Exception):
    def __init__(self, technician_or_pilot: str, aircraft_model: str) -> None:
        super().__init__(f"{technician_or_pilot} is not authorized for aircraft model {aircraft_model}")
