import copy
from stringprep import b1_set

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports() #tutti gli aeroporti
        self._idMapAirports = {} #mappa tra id aereoporti e aeroporti
        for a in self._airports:
            self._idMapAirports[a.ID] = a

        self._bestCammino = []
        self._bestScore = 0


    def getCamminoOttimo(self, v0, v1, t):
        self._bestCammino = []
        self._bestScore = 0

        parziale = [v0]
        self._ricorsione(parziale, v1, t)

        return self._bestCammino, self._bestScore

    def ricorsione(self, parziale, v1, t):
        #verifico se parziale è una soluzione valida, ed in caso la salvo
        if parziale[-1] == v1:#allora arrivato ad aeroporto di destinazione; potenzialmente sol accettabile
            if self._getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        #verifico se ha senso continuare ad aggiungere elementi in parziale, oppure esco
        if len(parziale) == t+1: #allora parziale ha già raggiunto il numero massimo di tratte, non posso andare avanti
            return

        #espando parziale e faccio ricorsione con backtracking
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()

    def getScore(self, parziale):
        sumPesi = 0;
        for i in range(0, len(parziale)-1): #cicliamo su archi
            sumPesi += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return sumPesi

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        self.addEdges()
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        self._graph.clear_edges()
        self.addEdgesV2()
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")

    def addEdges(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        #Queste tratte hanno 2 problemi: i) ho archi diretti

        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                #allora posso aggiungerlo
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]['weight'] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight = t.peso)

    def addEdgesV2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def getViciniOrdinati(self, source):
        #restituidce tutti i vicini di source, ordinati per peso dell'arco che collega
        vicini = self._graph.neighbors(source)
        viciniT = []
        for v in vicini:
            viciniT.append((v, self._graph[source][v]["weight"]))
        viciniT.sort(key=lambda x: x[1], reverse=True)
        return viciniT

    def hasPath(self, v0, v1):
        #restituisce true se esiste cammino tre v0 e v1, altrimenti restituisce false
        return v1 in nx.node_connected_component(self._graph, v0) #componente connessa che contiene v0

    def getPath(self, v0, v1):
        #esplorare il grafo per esempio con bfs;
        #per ogni nodo (key) mi dice il nodo precedente nell'albero di visita
        #V1
        #dictOfPredecessors = dict(nx.bfs_predecessors(self._graph, v0))
        #path = [v1]
        #while path[0] != v0:
            #path.insert(0, dictOfPredecessors[path[0]])
        #path = [v0, ---- , v1] (parto dal fondo, poi metto predecessore di v1, poi predecessore del predecessore fino ad arrivare a v0)

        #V2
        #dictOfPredecessors = dict(nx.dfs_predecessors(self._graph, v0))
        #path = [v1]
        #while path[0] != v0:
            #path.insert(0, dictOfPredecessors[path[0]])

        #V3
        #path = nx.shortest_path(v0, v1)

        #V4
        #path = nx.dijkstra_path(self._graph, v0, v1, weight = None) #cammino minimo non guardando i pesi

        #V5
        path = nx.dijkstra_path(self._graph, v0, v1)
        return path


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes


