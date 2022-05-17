from random import sample
from algorithms import breadth_first_search as bfs, shortest_path as sp


class Landmarks:

    def __init__(self, G, k, method='r'):
        self._graph = G
        self._number_of_landmarks = k
        self._selection_method = method
        self._landmarks = self.__select_landmarks()
        self._dist = {}
        for l in self._landmarks:
            self._dist[l] = {}
            for u, d in bfs(self._graph, l):
                self._dist[l][u] = d

    def __select_landmarks(self):

        if self._number_of_landmarks > self._graph.number_of_vertices:
            raise ValueError("Number of landmarks is larger than the number of vertices")
        if self._selection_method == 'r':
            return sample(self._graph.vertices(), self._number_of_landmarks)
        elif self._selection_method == 'hd':
            return sorted(self._graph.vertices(), key=self._graph.degree)[-self._number_of_landmarks:]
        elif self._selection_method == 'bc':
            L = []
            # TODO: Analyse different strategies of selection of M
            M = self._graph.number_of_vertices
            P = set()
            # TODO: Analyse different strategies of sampling
            sample_pairs = zip(sample(self._graph.vertices(), M), sample(self._graph.vertices(), M))
            for pair in sample_pairs:
                P.add(sp(self._graph, *pair))
            VP = set().union(*map(set, P))
            for i in range(self._number_of_landmarks):
                c = {}
                for v in VP:
                    for p in P:
                        if v in p:
                            try:
                                c[v] += 1
                            except KeyError:
                                c[v] = 1
                l = max(c, key=lambda u: c[u])
                # Not removing the paths but instead removing the landmark from the set
                VP.remove(l)
                L.append(l)
            return L
        else:
            raise ValueError("Unknown landmarks selection method")

    def landmarks_basic(self, s, t):
        d_approx = self._graph.number_of_vertices-1
        for dl in self._dist.values():
            d_estimate = dl[s] + dl[t]
            if d_estimate < d_approx:
                d_approx = d_estimate
        return d_approx
