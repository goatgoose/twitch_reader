
class Graph:
    def __init__(self):
        self.nodes = {}  # node id : node

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, edge):
        tail = self.nodes[edge.nodes[0]]
        head = self.nodes[edge.nodes[1]]
        tail.edges[head.id] = edge

    def remove_edge(self, nodes):
        tail = self.nodes[nodes[0]]
        head_id = nodes[1]
        if head_id in tail.edges:
            del tail.edges[head_id]

    def edges(self):
        edges_set = set()
        for node in self.nodes.values():
            for edge in node.edges.values():
                edges_set.add(edge)
        return list(edges_set)

    def bfs(self, start_id):
        to_traverse = [self.nodes[start_id]]
        discovered = set()
        path = []

        while len(to_traverse) > 0:
            node = to_traverse.pop(0)
            if node not in discovered:
                path.append(node)
                discovered.add(node)

            for head in node.edges:
                neighbor = self.nodes[head]
                if neighbor not in discovered:
                    to_traverse.append(neighbor)

        return path

    def __getitem__(self, item):
        return self.nodes.get(item)

    def __str__(self):
        ret = ""
        for node in self.nodes.values():
            ret += f"{node.id}: "
            if len(node.edges) > 0:
                for edge in node.edges:
                    ret += f"{edge}, "
            else:
                ret += "-"
            ret += "\n"
        return ret


class UndirectedGraph(Graph):
    def add_edge(self, edge):
        node1 = self.nodes[edge.nodes[0]]
        node2 = self.nodes[edge.nodes[1]]
        node1.edges[node2.id] = edge
        node2.edges[node1.id] = edge

    def remove_edge(self, nodes):
        tail_id = nodes[0]
        tail = self.nodes[tail_id]
        head_id = nodes[1]
        head = self.nodes[head_id]

        if head_id in tail.edges:
            del tail.edges[head_id]
        if tail_id in head.edges:
            del head.edges[tail_id]

    def maximum_spanning_tree(self):
        edges = self.edges()
        edges.sort(reverse=True, key=lambda edge: edge.weight)


class Node:
    def __init__(self, id_):
        self.id = id_
        self.edges = {}  # head id : edge

    def __str__(self):
        return str(f"<{self.id}>")

    def __repr__(self):
        return str(self)


class Edge:
    def __init__(self, nodes):
        self.nodes = nodes


class WeightedEdge(Edge):
    def __init__(self, nodes, weight):
        super().__init__(nodes)
        self.weight = weight


if __name__ == '__main__':
    graph = UndirectedGraph()

    graph.add_node(Node(1))
    graph.add_node(Node(2))
    graph.add_node(Node(3))
    graph.add_node(Node(4))

    graph.add_edge(WeightedEdge([1, 2], 1))
    graph.add_edge(WeightedEdge([2, 3], 2))
    graph.add_edge(WeightedEdge([3, 2], 2))
    graph.add_edge(WeightedEdge([3, 4], 3))

    print(graph)
    print(graph.bfs(1))
