import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        durata= self._view.txt_durata.value

        if durata is None or durata == "":
            self._view.show_alert("Inserisci un numero!")
            return
        try:
            durata_minuti = int(durata)
        except ValueError:
            self._view.show_alert("Devi inserire un numero intero.")
            return
        self._model.build_graph(durata_minuti)
        self._view.lista_visualizzazione_1.controls.clear()
        n_nodi = self._model.get_num_of_nodes()
        n_archi = self._model.get_num_of_edges()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo creato: {n_nodi} Album, {n_archi} Archi")
        )
        self._view.dd_album.options.clear()
        for n in self._model._nodes:
            albums = ft.dropdown.Option(text=n.title, key=str(n.id))
            self._view.dd_album.options.append(albums)

        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        album_id = int(self._view.dd_album.value)

        self._model._album_cercato = self._model.dict_album[album_id]

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        a=self._model._album_cercato
        if a is None:
            self._view.show_alert("Seleziona un album ")
        n_vicini, durata_vicini = self._model.get_num_durata_neighbors(a)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Dimensione componente:{n_vicini}"))
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Durata totale:{durata_vicini:.2f} minuti"))
        self._view.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        a=self._model._album_cercato
        dtot=float(self._view.txt_durata_totale.value)
        lista_set,durata_tot=self._model.cerca_set_album(a,dtot)
        lunghezza_set=len(lista_set)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(
            ft.Text(f"Set trovato ({lunghezza_set} album, durata {durata_tot:.2f} minuti):"))
        for album in lista_set:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"-{album.title} ({(float(album.durata)/60000):.2f} min)")
            )
        self._view.update()