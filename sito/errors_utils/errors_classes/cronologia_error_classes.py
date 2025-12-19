class InvalidEventId(Exception):
    """
    errore nel trovare un evento
    """
    def __init__(self, identifier, by="id"):
        super().__init__(f"evento non trovato per {by}: {identifier}")
        self.identifier = identifier
        self.by = by



