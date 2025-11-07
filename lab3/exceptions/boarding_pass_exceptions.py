class InvalidBoardingPassException(Exception):
    def __init__(self, passport_number: str) -> None:
        super().__init__(f"No valid boarding pass found for passport {passport_number}")
