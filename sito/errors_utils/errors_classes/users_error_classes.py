class FailedSignUpError(Exception):
    """
    Eccezione sollevata quando la creazione di un utente fallisce.

    Attributes:
        message (str): Messaggio di errore.
    """

    def __init__(self, message: str):
        """
        Inizializza l'eccezione FailedSignUpError.

        Args:
            message (str): Messaggio di errore da associare all'eccezione.
        """
        self.message = message
        super().__init__(self.message)


class InitPasswordNotSetError(Exception):
    """
    Eccezione sollevata quando la password iniziale per l'admin starter non è stata impostata.

    Attributes:
        message (str): Messaggio di errore.
    """

    def __init__(self, message: str):
        """
        Inizializza l'eccezione InitPasswordNotSetError.

        Args:
            message (str): Messaggio di errore da associare all'eccezione.
        """
        self.message = message
        super().__init__(self.message)


class FailedLoginError(Exception):
    """
    Eccezione sollevata quando il login di un utente fallisce.

    Attributes:
        message (str): Messaggio di errore.
    """

    def __init__(self, message: str):
        """
        Inizializza l'eccezione FailedLoginError.

        Args:
            message (str): Messaggio di errore da associare all'eccezione.
        """
        self.message = message
        super().__init__(self.message)
