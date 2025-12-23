from sito.modelli.classe import Classe
from ..modelli import Utente
from ..costanti import COEFFICIENTI_VOTI, SELECTORS, NOMI_CHECKBOX

def costruisci_json_studente(studente: Utente,data_str : str) -> dict:
    eventi = studente.cronologia_studente.filter_by(data=data_str).all()
    row = {
            "checkboxes":{nome : False for nome in NOMI_CHECKBOX},
            "selectors":{"Presenza":"Presente"},
            "voti":[],
            "frase":"",
            }

    for evento in eventi:
        if evento.attivita in NOMI_CHECKBOX:
            row["checkboxes"][evento.attivita]=True
        elif evento.attivita in SELECTORS:
            row["selectors"][evento.attivita]=evento.extra_info[evento.attivita]
        elif evento.attivita == "Voto":
            row["voti"].append({evento.extra_info[evento.attivita]
                                :evento.modifica_punti/COEFFICIENTI_VOTI[evento.extra_info[evento.attivita]]})
        elif evento.attivita == "Frase":
            row["frase"]=evento.extra_info["Frase"]
    return row

def costruisci_json_manage_data(nome_classe:str,data_str:str)-> list:
    studenti = Classe.da_nome(nome_classe).studenti.all()
    valori_studenti = [
            {"studente": studente,
             "valori":costruisci_json_studente(studente,data_str)}
            for studente in studenti
            ]
    valori_studenti.sort(key=lambda x: x["studente"].nominativo)
    return valori_studenti



