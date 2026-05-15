import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports() #tutti gli aeroporti
        self._idMapAirports = {} #mappa tra id aereoporti e aeroporti
        for a in self._airports:
            self._idMapAirports[a.ID] = a

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

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes


