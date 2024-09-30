class ClasseAlreadyExists(Exception):
    """
    errore per la creazione di classi già esistenti
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
