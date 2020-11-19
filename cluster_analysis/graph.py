
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
        return self._search(start_id, 0)

    def bfs_iter(self, start_id):
        for node in self._search_iter(start_id, 0):
            yield node

    def dfs(self, start_id):
        return self._search(start_id, -1)

    def dfs_iter(self, start_id):
        return self._search_iter(start_id, -1)

    def _search(self, start_id, pop_index):
        path = []
        for node in self._search_iter(start_id, pop_index):
            path.append(node)
        return path

    def _search_iter(self, start_id, pop_index):
        to_traverse = [self.nodes[start_id]]
        discovered = set()

        while len(to_traverse) > 0:
            node = to_traverse.pop(pop_index)
            if node not in discovered:
                yield node
                discovered.add(node)

            for head in node.edges:
                neighbor = self.nodes[head]
                if neighbor not in discovered:
                    to_traverse.append(neighbor)

    def is_cyclic(self):
        if len(self.nodes) == 0:
            return False

        checked = set()
        while len(checked) < len(self.nodes):
            visited = set()
            start = set(self.nodes.keys()).difference(checked).pop()
            prev = None
            for node in self.dfs_iter(start):
                for neighbor in node.edges:
                    if neighbor != prev and neighbor in visited:
                        return True
                visited.add(node.id)
                prev = node.id
            checked = checked.union(visited)

        return False

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

    def copy(self):
        new_graph = self.__class__()
        for id_ in self.nodes:
            new_graph.nodes[id_] = Node(self.nodes[id_].id)
        for edge in self.edges():
            new_graph.add_edge(edge.copy())
        return new_graph


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
        st = UndirectedGraph()
        for node in self.nodes.values():
            st.add_node(Node(node.id))

        edges = self.edges()
        edges.sort(reverse=True, key=lambda edge: edge.weight)

        while len(edges) > 0:
            to_add = edges.pop(0).copy()
            st.add_edge(to_add)
            if st.is_cyclic():
                st.remove_edge(to_add.nodes)
        return st

class Node:
    def __init__(self, id_):
        self.id = id_
        self.edges = {}  # head id : edge

    def __str__(self):
        return str(f"<{self.id}>")

    def __repr__(self):
        return str(self)

    def copy(self):
        node = Node(self.id)
        for id_ in self.edges:
            node.edges[id_] = self.edges[id_].copy()
        return node


class Edge:
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return str(self.nodes)

    def __repr__(self):
        return str(self)

    def copy(self):
        return Edge(self.nodes)


class WeightedEdge(Edge):
    def __init__(self, nodes, weight):
        super().__init__(nodes)
        self.weight = weight

    def __str__(self):
        return super().__str__() + f" - ({self.weight})"

    def copy(self):
        return WeightedEdge(self.nodes, self.weight)


if __name__ == '__main__':
    graph = UndirectedGraph()

    graph.add_node(Node(1))
    graph.add_node(Node(2))
    graph.add_node(Node(3))
    graph.add_node(Node(4))

    graph.add_edge(WeightedEdge([1, 2], 1))
    graph.add_edge(WeightedEdge([2, 3], 2))
    graph.add_edge(WeightedEdge([3, 4], 2))
    graph.add_edge(WeightedEdge([4, 1], 3))
    graph.add_edge(WeightedEdge([2, 4], 10))

    print(graph)

    st = graph.maximum_spanning_tree()
    print(st)
