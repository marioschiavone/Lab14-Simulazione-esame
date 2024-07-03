import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self._allChromosomes = DAO.getAllChromosomes()
        self._allConnectedGenes=DAO.getAllConnectedGenes()
        self._allGenes=DAO.getAllGenes()

        self.solBest=[]

        self._idMap={}
        for g in self._allGenes:
            self._idMap[g.GeneID]=g.Chromosome

    def searchPath(self, t):

        for n in self._grafo.nodes:
            partial = []
            partial_edges = []

            partial.append(n)
            self.ricorsione(partial, partial_edges, t)

        print("final", len(self.solBest), [i[2]["weight"] for i in self.solBest])

    def ricorsione(self, partial, partial_edges, t):
        n_last = partial[-1]
        neigh = self.getAdmissibleNeighbs(n_last, partial_edges, t)

        # stop
        if len(neigh) == 0:
            weight_path = self.computeWeightPath(partial_edges)
            weight_path_best = self.computeWeightPath(self.solBest)
            if weight_path > weight_path_best:
                self.solBest = partial_edges[:]
            return

        for n in neigh:
            partial.append(n)
            partial_edges.append((n_last, n, self._grafo.get_edge_data(n_last, n)))
            self.ricorsione(partial, partial_edges, t)
            partial.pop()
            partial_edges.pop()

    def getAdmissibleNeighbs(self, n_last, partial_edges, t):
        all_neigh = self._grafo.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if e[2]["weight"] > t:
                e_inv = (e[1], e[0], e[2])
                if (e_inv not in partial_edges) and (e not in partial_edges):
                    result.append(e[1])
        return result

    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight


    def buildGraph(self):
        self._grafo.clear()
        for chromosome in self._allChromosomes:
            self._nodes.append(chromosome)
        self._grafo.add_nodes_from(self._nodes)
        edges={}
        for g1, g2, corr in self._allConnectedGenes:
            if (self._idMap[g1], self._idMap[g2]) not in edges:
                edges[(self._idMap[g1], self._idMap[g2])]=float(corr)
            else:
                edges[(self._idMap[g1], self._idMap[g2])] += float(corr)
        for key, value in edges.items():
            self._edges.append((key[0], key[1], value))
        self._grafo.add_weighted_edges_from(self._edges)
    def countEdges(self, soglia):
        count_bigger=0
        count_smaller=0
        for edge in self._grafo.edges(data=True):
            if edge[2]['weight']>soglia:
                count_bigger += 1
            elif edge[2]['weight']<soglia:
                count_smaller += 1
        return count_bigger, count_smaller

    def getMinWeight(self):
        return min(x[2]['weight'] for x in self._grafo.edges(data=True))
    def getMaxWeight(self):
        return max(x[2]['weight'] for x in self._grafo.edges(data=True))
    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
