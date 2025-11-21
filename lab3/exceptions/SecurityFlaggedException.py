class SecurityFlaggedException(Exception):
    def __init__(self, passenger_name: str, reason: str) -> None:
        super().__init__(f"{passenger_name} is flagged by security: {reason}")

