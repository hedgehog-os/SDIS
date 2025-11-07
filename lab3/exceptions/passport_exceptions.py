class InvalidPassportException(Exception):
    def __init__(self, passport_number: str) -> None:
        super().__init__(f"Passport {passport_number} is expired or invalid.")

class DuplicatePassengerException(Exception):
    def __init__(self, passport_number: str) -> None:
        super().__init__(f"Passenger with passport {passport_number} is already on board")
