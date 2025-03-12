class Graph:
    def __init__(self):
        self.nodes = set()
        self.adjacency_list = {}
        self.neighbor_matrix = []

    def add_node(self, node):
        pass

    def remove_node(self, node):
        pass

    def add_edge(self, node1, node2, weight=1.0):
        pass

    def remove_edge(self, node1, node2):
        pass

    def get_neighbors(self, node):
        pass

    def has_edge(self, node1, node2):
        pass

    def get_edge_weight(self, node1, node2):
        pass

    def bfs(self, start_node, use_adjacency_list=True):
        pass

    def connected_components(self):
        pass