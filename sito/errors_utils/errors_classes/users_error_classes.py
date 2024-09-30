class UserAlreadyExists(Exception):
    """
    errore per la creazione di utenti già esistenti
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InitPasswordNotSet(Exception):
    """
    errore per la passoword init dell' admin starter
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
