import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.album_selezonato = None

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        durata_min=self._view.txt_durata.value
        durata=int(durata_min)*60000
        self._model.build_graph(durata)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(
            f"Grafo creato: {self._model.G.number_of_nodes()} album, {self._model.G.number_of_edges()} archi"))
        albums = self._model.G.nodes()
        self._view.dd_album.options.clear()
        for album in albums:
            self._view.dd_album.options.append(ft.dropdown.Option(key=album.id, text=str(album.title)))
        self._view.update()


    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        id_album=int(self._view.dd_album.value)
        self.album_selezonato=self._model.dict_nodes.get(id_album)


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        if not self.album_selezonato:
            self._view.show_alert("Selezionare un album")
            return
        componente=self._model.get_componente(self.album_selezonato)
        durata_totale=0
        for c in componente:
            durata_totale+=c.durata
        durata_min=durata_totale/60000
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente: {len(componente)}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Durata totale: {durata_min:.2f}"))
        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        durata_massima_min=int(self._view.txt_durata_totale.value)
        durata_massima=durata_massima_min*60000
        soluzione_migliore=self._model.get_percorso_migliore(self.album_selezonato,durata_massima)
        durata_soluz=0
        for album in soluzione_migliore:
            durata_soluz+=(album.durata/60000)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(
            f"Set trovato ({len(soluzione_migliore)} album, durata {durata_soluz:.2f} minuti):"))
        for album in soluzione_migliore:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(
                f"-{album.title} ({(album.durata/60000):.2f} min)"))
        self._view.update()