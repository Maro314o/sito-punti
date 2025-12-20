class InvalidEventId(Exception):
    """
    Eccezione sollevata quando non si riesce a trovare un evento specificato.

    Attributes:
        identifier (Any): Identificatore dell'evento non trovato.
        by (str): Tipo di identificatore utilizzato (default "id").
    """

    def __init__(self, identifier, by: str = "id"):
        """
        Inizializza l'eccezione InvalidEventId.

        Args:
            identifier (Any): Identificatore dell'evento che non è stato trovato.
            by (str, optional): Tipo di identificatore utilizzato (ad esempio "id" o "nome"). Defaults to "id".
        """
        super().__init__(f"evento non trovato per {by}: {identifier}")
        self.identifier = identifier
        self.by = by
