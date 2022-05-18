"""Class for undirected graphs"""


class Graph:
    """Class for undirected graphs.

    Graphs hold undirected edges. Self loops are allowed but multiple
    (parallel) edges are not.

    Parameters
    ----------
    edge_list: input list of edges (optional)
        Data to initialise graph. Can be a text file containing edges (one per line separated by spaces)
        or a list/tuple of pairs of vertices. If not passed, an empty graph is created.

    Examples
    --------
    >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
    >>> print(G)
    {'A': {'B'}, 'B': {'C', 'A', 'E', 'D'}, 'C': {'E', 'B'}, 'D': {'B'}, 'E': {'C', 'B'}}
    """

    def __init__(self, edge_list=None):
        self._adjacency_dict = {}
        if edge_list is not None:
            if isinstance(edge_list, str):
                with open(edge_list, 'r') as el_file:
                    for edge in el_file.readlines():
                        self.add_edge(*(edge.split()))
            elif isinstance(edge_list, (tuple, list)):
                for edge in edge_list:
                    self.add_edge(*edge)
            else:
                raise TypeError(f'Cannot construct a graph from {type(edge_list)}')

    def __len__(self):
        """Returns the number of vertices in the graph."""
        return self.number_of_vertices

    def __repr__(self):
        """Returns the string representation of the adjacency dictionary of the graph"""
        return str(self._adjacency_dict)

    def add_edge(self, u, v):
        """Adds an edge to the graph.

        Parameters
        ----------
        u: vertex
        v: vertex

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> G.add_edge("D", "E")
        >>> print(G)
        {'A': {'B'}, 'B': {'A', 'E', 'C', 'D'}, 'C': {'B', 'E'}, 'D': {'B', 'E'}, 'E': {'B', 'C', 'D'}}
        """
        if u not in self._adjacency_dict:
            self._adjacency_dict[u] = {v}
        else:
            self._adjacency_dict[u].add(v)
        if v not in self._adjacency_dict:
            self._adjacency_dict[v] = {u}
        else:
            self._adjacency_dict[v].add(u)

    def add_vertex(self, v):
        """Adds a vertex to the graph.

        Parameters
        ----------
        v: vertex.

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> G.add_vertex("F")
        >>> print(G.vertices())
        {'E', 'A', 'F', 'D', 'B', 'C'}
        """
        if v not in self._adjacency_dict:
            self._adjacency_dict[v] = set()

    def remove_edge(self, u, v):
        """Removes an edge from the graph.

        Parameters
        ----------
        u: vertex
        v: vertex

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> G.remove_edge("B", "E")
        >>> print(G)
        {'A': {'B'}, 'B': {'C', 'D', 'A'}, 'C': {'E', 'B'}, 'D': {'B'}, 'E': {'C'}}
        """
        try:
            self._adjacency_dict[u].remove(v)
        except KeyError:
            raise ValueError(f'No edge ({u}, {v}) found in {self}')
        else:
            self._adjacency_dict[v].remove(u)

    def remove_vertex(self, v):
        """Removes a vertex from the graph.

        Parameters
        ----------
        v: vertex

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> G.remove_vertex("B")
        >>> print(G.vertices())
        {'D', 'E', 'C', 'A'}
        """
        for n in self.neighbors(v):
            self._adjacency_dict[n].remove(v)
        self._adjacency_dict.pop(v)

    def neighbors(self, v):
        """Returns all vertices adjacent to a vertex.

        Parameters
        ----------
        v: vertex

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> print(G.neighbors("B"))
        {'C', 'E', 'D', 'A'}
        """
        try:
            return self._adjacency_dict[v]
        except KeyError:
            raise ValueError(f'No vertex named {v} found in {self}')

    def degree(self, v):
        """Returns degree of a given vertex.

        Parameters
        ----------
        v: vertex

        Returns
        -------
        degree: int
            Number of edges incident to v (self-loops are counted twice)

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "B"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> print(G.degree("B"))
        5
        """
        neighbors = self.neighbors(v)
        return len(neighbors)+1 if v in neighbors else len(neighbors)

    def vertices(self):
        """Return the set of all vertices of the graph.

        Returns
        -------
        vertices: set

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> print(G.vertices())
        {'D', 'C', 'E', 'A', 'B'}
        """
        return set(self._adjacency_dict.keys())

    @property
    def number_of_vertices(self):
        """Returns the number of vertices in the graph.

        Returns
        -------
        n: int

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> print(G.number_of_vertices)
        5
        """
        return len(self.vertices())

    def subgraph(self, vertices):
        """Returns a subgraph of the graph constructed on given vertices.

        Parameters
        ----------
        vertices: iterable

        Returns
        -------
        sub: Graph

        Examples
        --------
        >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
        >>> print(G.subgraph(["E", "C", "A"]))
        {'E': {'C'}, 'C': {'E'}, 'A': set()}
        """
        sub = Graph()
        for v in vertices:
            sub.add_vertex(v)
            for n in self.neighbors(v):
                if n in vertices:
                    sub.add_edge(v, n)
        return sub
