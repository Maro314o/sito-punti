class FailedSignUpError(Exception):
    """
    errore per la creazione di utenti
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InitPasswordNotSetError(Exception):
    """
    errore per la passoword init dell' admin starter
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FailedLoginError(Exception):
    """
    errore per il login
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
