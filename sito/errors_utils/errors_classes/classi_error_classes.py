class ClasseAlreadyExistsError(Exception):
    """
    Eccezione sollevata quando si tenta di creare una classe
    che esiste già nel database.

    Attributes:
        message (str): Messaggio di errore.
    """

    def __init__(self, message: str):
        """
        Inizializza l'eccezione ClasseAlreadyExistsError.

        Args:
            message (str): Messaggio di errore da associare all'eccezione.
        """
        self.message = message
        super().__init__(self.message)
