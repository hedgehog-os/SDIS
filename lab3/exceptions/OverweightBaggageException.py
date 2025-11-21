class OverweightBaggageException(Exception):
    def __init__(self, tag_number: str, weight: float, limit: float) -> None:
        super().__init__(f"Baggage {tag_number} exceeds weight limit: {weight}kg > {limit}kg.")

