import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._years = []
        self._teams = []

        self._graph = nx.Graph()
        self._bestPath = []
        self._totValue = 0

    def handlePercorso(self, team):
        self._bestPath = []
        self._bestScore = 0

        parziale = [team]
        self._ricorsione(parziale, float("inf"), 0)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, ultimoPeso, pesoTotale):

        if pesoTotale > self._bestScore:
            self._bestScore = pesoTotale
            self._bestPath = copy.deepcopy(parziale)

        for n in self._graph.neighbors(parziale[-1]):
            peso_arco = self._graph[n][parziale[-1]]["weight"]

            if n not in parziale and peso_arco < ultimoPeso:
                parziale.append(n)
                self._ricorsione(parziale, peso_arco, pesoTotale + peso_arco)
                parziale.pop()

    def getEdgeWeight(self, n1, n2):
        return self._graph[n1][n2]["weight"]



    def buildGraph(self):
        self._graph.add_nodes_from(self._teams)

        for n in self._graph:
            for m in self._graph:
                if n != m:
                    self._graph.add_edge(n, m, weight=n.salaries + m.salaries)


    def getNeighbours(self, team):

        neighTeams = []

        for n in self._graph.neighbors(team):
            neighTeams.append(
                (n, self._graph[n][team]["weight"])
            )

        neighTeams.sort(key=lambda x: x[1], reverse=True)

        return neighTeams



    def getAllYears(self):
        self._years = DAO.getAllYears()
        return self._years

    def getAllTeams(self, year):
        self._teams = DAO.getAllNodes(year)
        return self._teams

    def _getGraphDetails(self):
        nodes = self._graph.nodes()
        edges = self._graph.edges()
        return nodes, edges