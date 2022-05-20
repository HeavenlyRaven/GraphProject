"""Basic graph algorithms"""
from collections import deque


def breadth_first_search(G, s):
    """Iterate over edges in a breadth-first-search (BFS)

    Parameters
    ----------
    G: Graph

    s: vertex
        Starting node for the breadth-first search; this function
        iterates over only those edges in the component reachable from
        this node.

    Yields
    ------
    (u, data): tuple of 2 elements
        u: vertex
            A vertex visited during the traversal.
        data: tuple of 2 elements
            p: vertex
                Predcessor of vertex u in the traversal.
            d: int
                Shortest distance from s to u (minimum number of edges between s and u)

    Examples
    --------
    >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
    >>> print(list(breadth_first_search(G, "A")))
    [('A', (None, 0)), ('B', ('A', 1)), ('E', ('B', 2)), ('C', ('B', 2)), ('D', ('B', 2))]
    """
    visited = set()
    queue = deque([(s, None, 0)])
    while queue:
        u, p, d = queue.popleft()
        if u not in visited:
            visited.add(u)
            yield u, (p, d)
            for v in G.neighbors(u):
                if v not in visited:
                    queue.append((v, u, d+1))


def shortest_path(G, s, t):
    """Return the shortest path between two vertices.

    Parameters
    ----------
    G: Graph
    s: vertex
    t: vertex

    Returns
    -------
    path: tuple
        Tuple containing ordered vertices of a shortest path between s and t.

    Examples
    --------
    >>> G = Graph([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "E")])
    >>> print(shortest_path(G, "A", "E"))
    ('A', 'B', 'E')
    """
    prev = {}
    for u, data in breadth_first_search(G, t):
        prev[u] = data[0]
        if u == s:
            path = []
            while s is not None:
                path.append(s)
                s = prev[s]
            return tuple(path)
