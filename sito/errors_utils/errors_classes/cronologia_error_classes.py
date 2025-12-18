class InvalidEventId(Exception):
    """
    errore di id di un evento non esistente
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)



