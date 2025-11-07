class InvalidVisaException(Exception):
    def __init__(self, country: str) -> None:
        super().__init__(f"No valid visa for destination: {country}")
