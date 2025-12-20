from sito.costanti import NOT_AVALIDABLE
from .. import db


class Classe(db.Model):
    """
    Modello ORM che rappresenta una classe scolastica.

    Contiene informazioni sul numero massimo di studenti per squadra
    e le relazioni con squadre e studenti.
    """

    id = db.Column(db.Integer, primary_key=True)
    nome_classe = db.Column(db.String(150), unique=True)
    massimo_studenti_squadra = db.Column(db.Integer)

    squadre = db.relationship("Squadra", lazy="dynamic")
    studenti = db.relationship("Utente", lazy="dynamic")

    @classmethod
    def da_id(cls, id: int) -> "Classe":
        """
        Restituisce una classe dato l'ID.

        Args:
            id (int): ID della classe.

        Returns:
            Classe: Istanza della classe.

        Raises:
            NoResultFound: Se la classe non esiste.
        """
        return cls.query.filter_by(id=id).one()

    @classmethod
    def da_nome(cls, nome_classe: str) -> "Classe":
        """
        Restituisce una classe dato il nome.

        Args:
            nome_classe (str): Nome della classe.

        Returns:
            Classe: Istanza della classe.

        Raises:
            NoResultFound: Se la classe non esiste.
        """
        return cls.query.filter_by(nome_classe=nome_classe).one()

    @classmethod
    def esiste_da_id(cls, id: int) -> "Classe | None":
        """
        Verifica se esiste una classe dato l'ID.

        Args:
            id (int): ID della classe.

        Returns:
            Classe | None: Classe se esiste, altrimenti None.
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def esiste_da_nome(cls, nome_classe: str) -> "Classe | None":
        """
        Verifica se esiste una classe dato il nome.

        Args:
            nome_classe (str): Nome della classe.

        Returns:
            Classe | None: Classe se esiste, altrimenti None.
        """
        return cls.query.filter_by(nome_classe=nome_classe).first()

    @classmethod
    def elenco_classi(cls) -> list["Classe"]:
        """
        Restituisce l'elenco di tutte le classi.

        Returns:
            list[Classe]: Lista di tutte le classi.
        """
        return cls.query.all()

    @classmethod
    def elenco_classi_studenti(cls) -> list["Classe"]:
        """
        Restituisce l'elenco delle classi degli studenti.

        Esclude le classi il cui nome è presente nella costante NOT_AVALIDABLE.

        Returns:
            list[Classe]: Lista delle classi valide per gli studenti.
        """
        return cls.query.filter(cls.nome_classe.notin_(NOT_AVALIDABLE)).all()
