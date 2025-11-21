class InvalidPassportException(Exception):
    def __init__(self, passport_number: str) -> None:
        super().__init__(f"Passport {passport_number} is expired or invalid.")

