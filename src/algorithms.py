from collections import deque


def breadth_first_search(G, s, with_prev=False):
    visited = set()
    queue = deque([(s, None, 0)])
    while queue:
        u, p, d = queue.popleft()
        if u not in visited:
            visited.add(u)
            if with_prev:
                yield u, p, d
            else:
                yield u, d
            for v in G.neighbors(u):
                if v not in visited:
                    queue.append((v, u, d+1))


def shortest_path(G, s, t):
    prev = {}
    for u, p, _ in breadth_first_search(G, s, with_prev=True):
        prev[u] = p
        if u == t:
            path = []
            while t is not None:
                path.append(t)
                t = prev[t]
            return tuple(path)
