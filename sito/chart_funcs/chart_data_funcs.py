def list_data(Cronologia, stagione):
    return [x.punti_cumulativi for x in Cronologia if x.stagione == stagione]


def list_label(Cronologia, stagione):
    return [x.data for x in Cronologia if x.stagione == stagione]


def list_attivita(Cronologia, stagione):
    return [x.attivita for x in Cronologia if x.stagione == stagione]
