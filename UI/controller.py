import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        # Controllo che l'utente abbia selezionato un mese
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        self._view.lst_result.controls.clear()
        # Recupero i dati del Model
        risultati = self._model.get_umidita_media(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese {self._mese} è:"))
        for r in risultati:
            self._view.lst_result.controls.append(ft.Text(f"{r['Localita']}: {r['Media']}")) # accediamo al valore associato alla chiave del dizionario
        self._view.update_page()

    def handle_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        sequenza_ottima, costo_minimo = self._model.calcola_sequenza(self._mese) # chiamiamo la ricorsione
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Coato totale: {costo_minimo}"))
        for s in sequenza_ottima:
            self._view.lst_result.controls.append(ft.Text(str(s)))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

