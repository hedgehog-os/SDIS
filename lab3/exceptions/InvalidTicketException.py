class InvalidTicketException(Exception):
    def __init__(self, ticket_code: str, reason: str = "Ticket validation failed") -> None:
        super().__init__(f"Ticket {ticket_code} is invalid: {reason}")

