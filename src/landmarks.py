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
        self._data = {l: dict(bfs(self._graph, l)) for l in self._landmarks}

    def __select_landmarks(self):

        if self._number_of_landmarks > len(self._graph):
            raise ValueError("Number of landmarks is larger than the number of vertices")
        if self._selection_method == 'r':
            return sample(self._graph.vertices(), self._number_of_landmarks)
        if self._selection_method == 'hd':
            return sorted(self._graph.vertices(), key=self._graph.degree)[-self._number_of_landmarks:]
        if self._selection_method == 'bc':
            # TODO: Analyse different strategies of selection of M
            M = len(self._graph)
            # TODO: Analyse different strategies of sampling
            sample_pairs = zip(sample(self._graph.vertices(), M), sample(self._graph.vertices(), M))
            c = {}
            for pair in sample_pairs:
                for v in sp(self._graph, *pair):
                    try:
                        c[v] += 1
                    except KeyError:
                        c[v] = 1
            return sorted(c.keys(), key=c.get)[-self._number_of_landmarks:]
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
        for dl in self._data.values():
            d_estimate = dl[s][1] + dl[t][1]
            if d_estimate < d_approx:
                d_approx = d_estimate
        return d_approx

    def __path_to(self, l, s, p):
        """Returns the path in the SPT for l from the vertex s
           to the closest vertex q belonging to path p
        """
        res = [s]
        while s not in p:
            s = self._data[l][s][0]
            res.append(s)
        return tuple(res)

    def landmarks_lca(self, s, t):
        """Landmarks-LCA algorithm

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
        >>> print(L.landmarks_lca("A", "E"))
        2
        """
        d_approx = len(self._graph)-1
        for l in self._landmarks:
            path_1 = self.__path_to(l, s, (l,))
            path_2 = self.__path_to(l, t, path_1)
            path_3 = self.__path_to(l, s, (path_2[-1], ))
            d_estimate = len(path_2) + len(path_3) - 2
            if d_estimate < d_approx:
                d_approx = d_estimate
        return d_approx
