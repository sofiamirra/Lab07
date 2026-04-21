from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self._dati_meteo = []
        self._best_sequenza = []
        self._best_costo = float("inf")

    """Fa da tramite tra il Controller e il DAO"""
    def get_umidita_media(self, mese):
        return MeteoDao().get_umidita_media(mese)

    def calcola_sequenza(self, mese):
        self._dati_meteo = MeteoDao.get_tutti_meteo_mese(mese)
        self._best_sequenza = []
        self._best_costo = float("inf")
        self._ricorsione([], 0)
        return self._best_sequenza, self._best_costo

    # PARZIALE: lista delle città visitate finora
    # LIVELLO: indica in quale giorno ci troviamo
    def ricorsione(self, parziale, livello):
        # condizione terminale: se siamo al 15esimo giorno calcola tutta la trasferta
        if livello == 15:
            costo = self._calcola_costo(parziale)
            if costo < self._best_costo: # se questo è il costo più basso visto finora
                self._best_costo = costo # la sequenza è la vincitrice e il costo è il nuovo migliore
                self._best_sequenza = list(parziale)
            return
        # condizione ricorsiva: l'esploratore deve decidere tra Milano, Torino e Genova
        citta_possibili = self._get_citta_giorno(livello)
        for prova in citta_possibili:
            if self._vincoli_soddisfatti(parziale, prova):
                parziale.append(prova) # aggiungo la città alla sequenza
                self._ricorsione(parziale, livello + 1)  # ricorsione sulle componenti future
                parziale.pop()

    def vincoli_soddisfatti(self, parziale, citta):
        count = 0
        for fermata in parziale:
            if fermata.localita == citta.localita:
                count += 1
        if count >= 6:
            return False # limite massimo di 6 giorni, non può andare qui

        livello = len(parziale)
        if livello == 0:
            return True # il primo giorno puoi andare dove vuoi

        if livello < 3:
            return citta.localita == parziale[0].localita # limite minimo di 3 giorni, non può andare in un'altra città

        # Per poter cambiare città, dobbiamo averne fatte 3 uguali prima
        if citta.localita != parziale[livello-1].localita:
            if (parziale[livello-1].localita != parziale[livello-2].localita) or \
                (parziale[livello - 2].localita != parziale[livello - 3].località):
                return False # se non abbiamo fatto ancora tre giorni fissi non si può cambiare


    def calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            costo += parziale[i].umidita # costo variabile
            # costo fisso se cambio rispetto al giorno prima
            if i > 0 and parziale[i].localita != parziale[i - 1].localita:
                costo+= 100
        return costo

    def _get_citta_giorno(self, giorno):
        # Ritorna le 3 città disponibili per il giorno specificato (0-14)
        # I dati nel DB sono ordinati per data, quindi i primi 3 record sono il giorno 1, ecc.
        return self._dati_meteo[giorno * 3: giorno * 3 + 3]



