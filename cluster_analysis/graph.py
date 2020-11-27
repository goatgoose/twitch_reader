import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import time


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

    def is_cyclic_for_start(self, start):
        to_traverse = [self.nodes[start]]
        discovered = set()
        parent = {start: None}

        while len(to_traverse) > 0:
            node = to_traverse.pop(-1)
            prev = parent[node.id]

            discovered.add(node)

            for head in node.edges:
                neighbor = self.nodes[head]
                if neighbor in discovered:
                    if neighbor.id != prev:
                        return True
                else:
                    to_traverse.append(neighbor)
                    parent[neighbor.id] = node.id

        return False

    def disconnected_groups(self):
        if len(self.nodes) == 0:
            return []

        groups = []
        checked = set()
        while len(checked) < len(self.nodes):
            visited = set()
            start = set(self.nodes.keys()).difference(checked).pop()
            for node in self.dfs_iter(start):
                visited.add(node.id)
            checked = checked.union(visited)
            groups.append(visited)
        return groups

    def disconnected_graphs(self):
        graphs = []
        for group in self.disconnected_groups():
            new_graph = self.__class__()
            for node_id in group:
                new_graph.add_node(self.nodes[node_id])
            graphs.append(new_graph)
        return graphs

    def plot(self, k=None, scale=1):
        nx_g = nx.Graph()
        nx_g.add_edges_from([edge.nodes for edge in self.edges()])

        plt.figure(figsize=(50, 50))
        spring_layout = nx.spring_layout(nx_g, k=k, scale=scale)
        nx.draw(nx_g, spring_layout, with_labels=True, node_size=80, font_size=12)
        plt.show()

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
    def __init__(self):
        super().__init__()

    def add_node(self, node):
        super().add_node(node)

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

        for i, edge in enumerate(edges):
            print(f"{i} / {len(edges)}")
            to_add = edge.copy()
            st.add_edge(to_add)
            if st.is_cyclic_for_start(to_add.nodes[0]):
                st.remove_edge(to_add.nodes)
        return st

    def k_spanning_tree(self, k):
        st = self.maximum_spanning_tree()
        edges = st.edges()
        edges.sort(key=lambda edge: edge.weight)
        for i in range(k):
            st.remove_edge(edges[i].nodes)
        return st

    @staticmethod
    def k_spanning_tree_for_tree(k, st):
        new_st = st.copy()
        new_st.k_spanning_tree(k)
        return new_st

    @staticmethod
    def hcs_clusters(g, clusters=[]):
        gs = [g_.copy() for g_ in g.disconnected_graphs()]
        for g_ in gs:
            if len(g_.nodes) == 1:
                clusters.append(g_)
                continue

            start = time.process_time()
            minimum_cut = g_.minimum_cut()
            print(f"min cut time: {time.process_time() - start}")
            if minimum_cut._stacked <= len(g_.nodes) / 2:
                to_delete = []
                for id_ in minimum_cut.nodes[0]:
                    edges = g_.nodes[id_].edges.values()
                    for edge in edges:
                        for node in edge.nodes:
                            if node in minimum_cut.nodes[1]:
                                to_delete.append(edge)
                while len(to_delete) > 0:
                    g_.remove_edge(to_delete.pop(-1).nodes)

                UndirectedGraph.hcs_clusters(g_, clusters)
            else:
                clusters.append(g_)
        return clusters

    def minimum_cut(self):
        # Karger's Algorithm
        min_cut = Edge([None, None])
        min_cut._stacked = len(self.nodes)

        trials = int((len(self.nodes) * (len(self.nodes) - 1)) / 2)
        # trials = (len(self.nodes) ** 2) * int(math.log(len(self.nodes)))
        for _ in range(trials):
            mc_graph = self.copy()
            for edge in mc_graph.edges():
                edge._stacked = 1

            while len(mc_graph.nodes) > 2:
                random_node = random.choice(list(mc_graph.nodes.values()))
                random_edge = random.choice(list(random_node.edges.values()))

                node1 = mc_graph[random_edge.nodes[0]]
                node2 = mc_graph[random_edge.nodes[1]]
                mc_graph.remove_edge([node1.id, node2.id])

                combined_ids = set()
                for node in [node1, node2]:
                    if hasattr(node, "_is_contraction_node"):
                        for id_ in node.id:
                            combined_ids.add(id_)
                    else:
                        combined_ids.add(node.id)

                contraction_node = Node(frozenset(combined_ids))
                contraction_node._is_contraction_node = True
                mc_graph.add_node(contraction_node)

                for node in [node1, node2]:
                    edges = list(node.edges.values())
                    for edge in edges:
                        tail = edge.nodes[0] if edge.nodes[0] != node.id else edge.nodes[1]
                        if tail in contraction_node.edges:
                            contraction_node.edges[tail]._stacked += edge._stacked
                        else:
                            new_edge = Edge([contraction_node.id, tail])
                            new_edge._stacked = edge._stacked
                            mc_graph.add_edge(new_edge)
                    while len(edges) > 0:
                        to_remove = edges.pop(-1)
                        mc_graph.remove_edge(to_remove.nodes)

                del mc_graph.nodes[node1.id]
                del mc_graph.nodes[node2.id]

            cut = mc_graph.edges()[0]
            if cut._stacked < min_cut._stacked:
                min_cut = cut

        if not isinstance(min_cut.nodes[0], frozenset):
            min_cut.nodes[0] = frozenset([min_cut.nodes[0]])
        if not isinstance(min_cut.nodes[1], frozenset):
            min_cut.nodes[1] = frozenset([min_cut.nodes[1]])
        return min_cut


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
        return Edge([node.copy() for node in self.nodes])


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
    graph.add_edge(WeightedEdge([3, 4], 3))
    graph.add_edge(WeightedEdge([4, 1], 4))
    graph.add_edge(WeightedEdge([1, 3], 4))

    graph.add_node(Node(5))
    graph.add_node(Node(6))
    graph.add_node(Node(7))

    graph.add_edge(WeightedEdge([4, 5], 4))
    graph.add_edge(WeightedEdge([5, 6], 4))
    graph.add_edge(WeightedEdge([6, 7], 4))
    graph.add_edge(WeightedEdge([7, 5], 4))

    clusters = UndirectedGraph.hcs_clusters(graph, [])
    print(graph)
    print([cluster.nodes for cluster in clusters])
    clusters = UndirectedGraph.hcs_clusters(graph, [])
    print(graph)
    print([[id_ for id_ in cluster.nodes] for cluster in clusters])

    # graph.plot()
