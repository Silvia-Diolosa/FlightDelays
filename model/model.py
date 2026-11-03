import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestCammino =[]
        self._bestScore = 0

    def getCamminoOttimo(self, v0, v1, t):
        self._bestCammino =[]
        self._bestScore = 0

        parziale = [v0]

        self._ricorsione(parziale, v1, t)
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1, t):
        #verifico se parziale è una soluzione valida,ed in caso la salvo
        if parziale[-1] == v1: # potenzialmente questa è una sol accettabile
            if self._getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        #verifico se ha senso continuare ad aggiungere elementi in parziale, oppure esco
        if len(parziale) == t+1: # allora parziale ha già raggiunto il numero massimo di tratte
            return

        #espando parziale e faccio ricorsione con backtracking
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()

    def _getScore(self, parziale):
        sumPesi = 0
        for i in range(0, len(parziale)-1):
            sumPesi += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return sumPesi

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}" )
        # self.addEdges()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}" )
        # self._graph.clear_edges()
        self.addEdgesV2()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}" )


    def addEdges(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        #Queste tratte hanno 2 problemi: i) ho archi diretti ed inversi,
        # e quindi dovrò fare la somma; ii) ho archi fra aeroporti che avevo filtrato

        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:  # se fa parte dei nodi filtrati okay
                #allora posso aggiungerlo.
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA): # se ha gia questo arco, incremento peso
                    self._graph[t.aeroportoP][t.aeroportoA]["weight"] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight = t.peso)

    def addEdgesV2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph: # sempre per vedere se fa parte dei nodi filtrati
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)


    def getViciniOrdinati(self, source):
        # Restituisce tutti i vicini di source, ordinati per peso dell'arco che collega source al vicino
        vicini = self._graph.neighbors(source)
        viciniT = []
        for v in vicini:
            viciniT.append( (v, self._graph[source][v]["weight"]) ) # crea tupla composta da vicino v e
                                                                # il peso dell'arco che collega v a source
        viciniT.sort(key = lambda x: x[1], reverse=True)
        return viciniT

    def hasPath(self, v0, v1):
        #Restituisce true se un qualche cammino fra v0 e v1 esiste, altrimenti restituisce False
        return v1 in nx.node_connected_component(self._graph, v0)
        #calcoliamo la componente connessa di v0, e verifichiamo se v1 è nella componente connessa (se si, sono connessi)

    def getPath(self, v0, v1):

        # #v1
        # dictOfPredecessors = dict(nx.bfs_predecessors(self._graph, v0)) #dizionario che per ogni chiave mi dice il suo predecessore
        # path = [v1]  #quindi parto dall'ultimo
        # while path[0] != v0: e finchè il primo elemento della lista è diverso da v0,
        #     path.insert(0, dictOfPredecessors[path[0]])  # continuo ad aggiungere elementi
        #

        # uguale a sopra con dfs
        # #v2
        # dictOfPredecessors = dict(nx.dfs_predecessors(self._graph, v0))
        # path = [v1]
        # while path[0] != v0:
        #     path.insert(0, dictOfPredecessors[path[0]])
        #

        # #v3
        # path = nx.shortest_path(v0, v1)

        #v4
        # path = nx.dijkstra_path(self._graph, v0, v1, weight = None)  #con none gli dico fregatene dei pesi

        #v5
        path = nx.dijkstra_path(self._graph, v0, v1)
        #path = [v0, -----, v1]

        return path


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes =  list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes