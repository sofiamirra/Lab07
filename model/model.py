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
    def _ricorsione(self, parziale, livello):
        # condizione terminale: se siamo al 15esimo giorno calcola tutta la trasferta
        if livello == 15:
            costo = self._calcola_costo(parziale)
            if costo < self._best_costo: # se questo è il costo più basso visto finora
                self._best_costo = costo # la sequenza è la vincitrice e il costo è il nuovo migliore
                self._best_sequenza = list(parziale)
            return
        # condizione ricorsiva: l'esploratore deve decidere tra Milano, Torino e Genova
        for citta in self._get_citta_giorno(livello):
            if self._vincoli_soddisfatti(parziale, citta):
                parziale.append(citta) # aggiungo la città alla sequenza
                self._ricorsione(parziale, livello + 1)  # ricorsione sulle componenti future
                parziale.pop()

    def _vincoli_soddisfatti(self, parziale, citta):
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
            return citta.localita == parziale[-1].localita # limite minimo di 3 giorni, non può andare in un'altra città

        # Per poter cambiare città, dobbiamo averne fatte 3 uguali prima
        if citta.localita != parziale[-1].localita:
            if not (parziale[-1].localita == parziale[-2].localita == parziale[-3].localita):
                return False # se non abbiamo fatto ancora tre giorni fissi non si può cambiare
        return True

    def _calcola_costo(self, parziale):
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
        data_giorno = self._dati_meteo[giorno * 3].data
        return [s for s in self._dati_meteo if s.data == data_giorno]


