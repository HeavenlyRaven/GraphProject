class Graph:

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

    def add_edge(self, u, v):
        if u not in self._adjacency_dict:
            self._adjacency_dict[u] = {v}
        else:
            self._adjacency_dict[u].add(v)
        if v not in self._adjacency_dict:
            self._adjacency_dict[v] = {u}
        else:
            self._adjacency_dict[v].add(u)

    def add_vertex(self, v):
        if v not in self._adjacency_dict:
            self._adjacency_dict[v] = set()

    def remove_edge(self, u, v):
        try:
            self._adjacency_dict[u].remove(v)
        except KeyError:
            raise ValueError(f'No edge ({u}, {v}) found in {self}')
        else:
            self._adjacency_dict[v].remove(u)

    def remove_vertex(self, v):
        for n in self.neighbors(v):
            self._adjacency_dict[n].remove(v)
        self._adjacency_dict.pop(v)

    def neighbors(self, v):
        try:
            return self._adjacency_dict[v]
        except KeyError:
            raise ValueError(f'No vertex named {v} found in {self}')

    def degree(self, v):
        return len(self.neighbors(v))

    def vertices(self):
        return self._adjacency_dict.keys()

    @property
    def number_of_vertices(self):
        return len(self.vertices())

    def subgraph(self, vertices):
        sub = Graph()
        for v in vertices:
            sub.add_vertex(v)
            for n in self.neighbors(v):
                if n in vertices:
                    sub.add_edge(v, n)
        return sub
