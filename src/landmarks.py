"""Class for Landmarks algorithms"""

from random import sample
from algorithms import breadth_first_search as bfs, shortest_path as sp


class Landmarks:
    """Class for Landmarks algorithms.

    This class contains methods for shortest path distances
    estimation based on algorithms using landmark vertices.

    Parameters
    ----------
    G: Graph

    k: int
        Number of landmarks to select.

    method: str
        Landmark selection method:
        'r'  : random selection
        'hd' : highest degree
        'bc' : best coverage

    Examples
    --------
    >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
    >>> L = Landmarks(G, 2, method='hd')
    """

    def __init__(self, G, k, method='r'):
        self._graph = G
        self._number_of_landmarks = k
        self._selection_method = method
        self._landmarks = self.__select_landmarks()
        self._dist = {}
        self._shortest_paths = {}
        for l in self._landmarks:
            self._dist[l] = {}
            self._shortest_paths[l] = {}
            for u, _, d in bfs(self._graph, l):
                self._dist[l][u] = d
                self._shortest_paths[l][u] = sp(G, l, u)

    def __select_landmarks(self):

        if self._number_of_landmarks > len(self._graph):
            raise ValueError("Number of landmarks is larger than the number of vertices")
        if self._selection_method == 'r':
            return sample(self._graph.vertices(), self._number_of_landmarks)
        elif self._selection_method == 'hd':
            return sorted(self._graph.vertices(), key=self._graph.degree)[-self._number_of_landmarks:]
        elif self._selection_method == 'bc':
            L = []
            # TODO: Analyse different strategies of selection of M
            M = len(self._graph)
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
        """Landmarks-Basic algorithm

        Parameters
        ----------
        s: vertex
        t: vertex

        Returns
        -------
        d_approx: int
            Approximate shortest path distance between s and t

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> L = Landmarks(G, 2, method='hd')
        >>> print(L.landmarks_basic("A", "E"))
        2
        """
        d_approx = len(self._graph)-1
        for dl in self._dist.values():
            d_estimate = dl[s] + dl[t]
            if d_estimate < d_approx:
                d_approx = d_estimate
        return d_approx

    def landmarks_LCA(self, s, t):
        d_approx = len(self._graph) - 1
        path = {}

        for l in self._landmarks:
            l_to_s_shortest_path = self._shortest_paths[l][s]
            l_to_t_shortest_path = self._shortest_paths[l][t]
            idx = 0
            while idx < len(l_to_s_shortest_path) and idx < len(l_to_t_shortest_path) and l_to_s_shortest_path[idx] == \
                    l_to_t_shortest_path[idx]:
                idx = idx + 1
            idx = idx - 1  # last equal node -> LCA
            LCA_to_s_shortest_path = l_to_s_shortest_path[idx::]
            s_to_LCA_shortest_path = LCA_to_s_shortest_path[::-1]
            LCA_to_t_shortest_path = l_to_t_shortest_path[idx + 1::]

            s_to_t_shortest_path = s_to_LCA_shortest_path + LCA_to_t_shortest_path

            idx_v = 0
            for v in s_to_LCA_shortest_path:
                v_neighbors = self._graph.neighbors(v)
                idx_u = 0
                for u in LCA_to_t_shortest_path:
                    if u in v_neighbors:
                        s_to_v = s_to_LCA_shortest_path[0:idx_v + 1]
                        u_to_t = LCA_to_t_shortest_path[idx_u:]
                        s_to_t = s_to_v + u_to_t
                        if len(s_to_t) < d_approx:
                            d_approx = len(s_to_t)
                            path = s_to_t
                    idx_u = idx_u + 1
                idx_v = idx_v + 1

            if len(s_to_t_shortest_path) < d_approx:
                d_approx = len(s_to_t_shortest_path)
                path = s_to_t_shortest_path
        return path
