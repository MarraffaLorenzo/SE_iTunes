import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.nodes=[]
        self.dict_nodes={}
        self.edges=[]
        self.G=nx.Graph()
        self.soluzione_migliore=[]


    def build_graph(self,durata):
        self.nodes=[]
        self.G.clear()
        self.dict_nodes={}
        self.edges=[]
        nodi=DAO.get_nodes(durata)
        for nodo in nodi:
            self.nodes.append(nodo)
            self.dict_nodes[nodo.id] = nodo
        self.G.add_nodes_from(self.nodes)
        connessioni=DAO.get_connessioni(self.dict_nodes)
        for connessione in connessioni:
            self.edges.append(connessione)

        self.G.add_edges_from(self.edges)

    def get_componente(self,album):
        if album not in self.G:
            return []
        return list(nx.node_connected_component(self.G, album))

    def get_percorso_migliore(self,a1,distanza):
        componente=self.get_componente(a1)
        self.soluzione_migliore=[]
        self.ricorsione(componente,[a1],a1.durata,distanza)
        return self.soluzione_migliore



    def ricorsione(self,componente,parziale,durata_corrente,durata_massima):
        if len(parziale)>len(self.soluzione_migliore):
            self.soluzione_migliore=parziale.copy()

        for album in componente:
            if album in parziale:
                continue
            nuova_durata=durata_corrente+album.durata
            if nuova_durata<=durata_massima:
                parziale.append(album)
                self.ricorsione(componente,parziale,nuova_durata,durata_massima)
                parziale.pop()

