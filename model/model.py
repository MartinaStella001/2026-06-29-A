import copy

import networkx as nx

from database.DAO import DAO
from model import cliente


class Model:
    def __init__(self):
        self._grafo= nx.DiGraph()
        self._idMapClienti = {}
        self._clienti = []
        self._bestPath = []

    def getAllCountries(self):
        return DAO.getAllCountries()

    def creaGrafo(self, country):
        self._grafo.clear()
        self._clienti = DAO.getAllNodes(country)
        for c in self._clienti:
            self._idMapClienti[c.CustomerId] = c
        self._grafo.add_nodes_from(self._clienti)
        self.addEdges(country)

    def addEdges(self, country):
        self._edges = DAO.getAllEdges(country, self._idMapClienti)
        for e in self._edges:
            if e.cliente1.fatturatoTot > e.cliente2.fatturatoTot:
                self._grafo.add_edge(e.cliente1, e.cliente2, weight=e.cliente1.fatturatoTot + e.cliente2.fatturatoTot)
            elif e.cliente1.fatturatoTot == e.cliente2.fatturatoTot:
                self._grafo.add_edge(e.cliente1, e.cliente2, weight=e.cliente1.fatturatoTot + e.cliente2.fatturatoTot)
                self._grafo.add_edge(e.cliente2, e.cliente1, weight=e.cliente1.fatturatoTot + e.cliente2.fatturatoTot)
            else:
                self._grafo.add_edge(e.cliente2, e.cliente1, weight=e.cliente1.fatturatoTot + e.cliente2.fatturatoTot)

    def getDettagliGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def stampaInfo(self):

        tupleClintiInfl= []
        for n in self._clienti:
            pesoEntranti = 0
            pesoUscenti = 0
            predecessori = self._grafo.predecessors(n)
            for p in predecessori:
                pesoEntranti+= self._grafo[p][n]["weight"]
            successori = self._grafo.successors(n)
            for s in successori:
                pesoUscenti+= self._grafo[n][s]["weight"]

            tupleClintiInfl.append((n, pesoUscenti- pesoEntranti))
        tupleClintiInfl.sort(key=lambda x: x[1], reverse=True)
        return tupleClintiInfl[0]

    def best5archi(self):
        tupleClienti = []
        for u,v,data in self._grafo.edges(data=True):
            tupleClienti.append((u,v,data["weight"]))
        tupleClienti.sort(key=lambda x: x[2], reverse=True)
        return tupleClienti[:5]

    def getAllClienti(self):
        return self._clienti

    def _getPath(self, source):
        self._bestPath = []
        parziale = [source]

        self._ricorsione(parziale)
        listaFatturati =[]
        for n in self._bestPath:
            listaFatturati.append((n,n.fatturatoTot))
        fatturatoComplessivo = self.getTotfatt()
        return listaFatturati, fatturatoComplessivo

    def _ricorsione(self, parziale):
        if len(parziale)-1 > len(self._bestPath)-1:
            self._bestPath = copy.deepcopy(parziale)

        for n in nx.neighbors(self._grafo, parziale[-1]):
            if n.fatturatoTot <= parziale[-1].fatturatoTot and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

    def getTotfatt(self):
        totFatt = 0
        for n in self._bestPath:
            totFatt += n.fatturatoTot
        return totFatt