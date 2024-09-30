class InvalidSeasonError(Exception):
    """
    errore di stagione non valida
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
