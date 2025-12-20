class InvalidSeasonError(Exception):
    """
    Eccezione sollevata quando viene specificata una stagione non valida.

    Attributes:
        message (str): Messaggio di errore.
    """

    def __init__(self, message: str):
        """
        Inizializza l'eccezione InvalidSeasonError.

        Args:
            message (str): Messaggio di errore da associare all'eccezione.
        """
        self.message = message
        super().__init__(self.message)
