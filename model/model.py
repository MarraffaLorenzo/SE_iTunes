import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.Graph()
        self._nodes=[]
        self._edges=[]

        self.dict_album={}
        self.lista_album=[]
        self.lista_connessioni=[]

        self.soluzione_migliore=[]

    def build_graph(self,durata):
        self.G.clear()
        self._nodes=[]
        self._edges=[]
        self.lista_album = []
        self.lista_connessioni = []
        self.dict_album = {}
        self._album_cercato = None

        album=DAO.get_album()
        for a in album:
            if (int(a.durata)/60000)>int(durata):
                self.lista_album.append(a)
                self.dict_album[a.id] = a

        self.lista_connessioni=DAO.get_connessioni(self.dict_album)

        for album in self.lista_album:
            self._nodes.append(album)
        self.G.add_nodes_from(self._nodes)

        self.G.add_edges_from(self.lista_connessioni)

    def get_num_durata_neighbors(self,a0):
        connessi = nx.node_connected_component(self.G, a0)
        dimensione=len(connessi)
        durata_totale=0
        for album in connessi:
            durata_totale+=float(album.durata)
        durata_minuti=durata_totale/60000

        return dimensione,durata_minuti

    def cerca_set_album(self,a1,dtot):
        conn=[]
        connessi=nx.node_connected_component(self.G, a1)
        for c in connessi:
            conn.append(c)
        conn.remove(a1)
        conn.sort(key=lambda a: a.durata)

        self.soluzione_migliore=[]
        parziale=[a1]

        durata_minuti_a1=float(a1.durata)/60000

        self.ricorsione(parziale,conn, dtot)
        durata_tot_soluzione=sum(float(a.durata) for a in self.soluzione_migliore)/60000

        return self.soluzione_migliore,durata_tot_soluzione

    def ricorsione(self,parziale,connessi, dtot):

        durata_corrente=sum(float(a.durata) for a in parziale)/60000

        if len(parziale)>len(self.soluzione_migliore):
            self.soluzione_migliore=list(parziale)

        if len(connessi)==0:
            return
        lungh_conn=len(connessi)
        if len(parziale)+lungh_conn<=len(self.soluzione_migliore):
            return

        for i in range(len(connessi)):

            album_attuale=connessi[i]
            durata_min=float(album_attuale.durata)/60000

            if durata_corrente+durata_min<=dtot:
                parziale.append(album_attuale)

                self.ricorsione(parziale,connessi[i+1:], dtot)

                parziale.pop()





















    def get_nodes(self):
        return self.G.nodes()

    def get_edges(self):
        return list(self.G.edges(data=True))

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()



