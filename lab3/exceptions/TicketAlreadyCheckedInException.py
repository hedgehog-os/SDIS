class TicketAlreadyCheckedInException(Exception):
    def __init__(self, ticket_id: str) -> None:
        super().__init__(f"Ticket {ticket_id} has already been checked in.")

