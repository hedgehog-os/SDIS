class TicketAlreadyCheckedInException(Exception):
    def __init__(self, ticket_id: str) -> None:
        super().__init__(f"Ticket {ticket_id} has already been checked in.")

class InvalidTicketException(Exception):
    def __init__(self, ticket_code: str, reason: str = "Ticket validation failed") -> None:
        super().__init__(f"Ticket {ticket_code} is invalid: {reason}")
