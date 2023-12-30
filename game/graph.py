from __future__ import annotations

class WeightedDirectedMultiGraph:
    class Node:
        def __init__(self, value) -> None:
            self.value = value


    def __init__(self) -> None:
        self.graph: dict[self.Node, dict[self.Node, list[int]]] = {}

    
    def add_node(self, value) -> Node:
        node = self.Node(value)

        if node not in self.graph:
            self.graph[node] = {}
        
        return node
    

    def remove_node(self, node: Node) -> None:
        for edge, weights in self.graph[node].items():
            for weight in weights:
                self.remove_edge(node, edge, weight)
        
        self.graph.pop(node)
    

    def __delitem__(self, node: Node) -> None:
        self.remove_node(node)
    

    @property
    def nodes(self) -> set[Node]:
        return self.graph.keys()
    

    def __iter__(self):
        return self.graph.__iter__()
    

    def __next__(self):
        return self.graph.__next__()
    

    def __contains__(self, node: Node) -> bool:
        for i in self.graph:
            if i is node:
                return True
        
        return False
    

    def __len__(self) -> int:
        return len(self.graph)
    

    def __add__(self, other: Graph) -> Graph:
        new_graph = Graph()
        for node, edges in self.graph:
            new_graph.graph[node] = edges
        
        for node, edges in other.graph:
            new_graph.graph[node] = edges
        
        return new_graph
    

    def add_edge(self, node1: Node, node2: Node, weight: int) -> None:
        self.add_node(node1)
        self.add_node(node2)

        if self.graph[node1][node2] is None:
            self.graph[node1][node2] = [weight]
            self.graph[node2][node1] = [-weight]
        else:
            self.graph[node1][node2].append(weight)
            self.graph[node2][node1].append(-weight)
    

    def remove_edge(self, node1: Node, node2: Node, weight: int) -> None:
        self.graph[node1][node2].remove(weight)
        self.graph[node2][node1].remove(-weight)

    
    def find_edge(self, node1: Node, node2: Node, weight: int) -> bool:
        if node2 in self.graph[node1]:
            return weight in self.graph[node1][node2]
    
        return False


    def get_edges(self, node: Node) -> dict[Node, list[int]]:
        return self.graph[node]
    
    
    def __getitem__(self, node: Node) -> dict[Node, list[int]]:
        return self.get_edges(node)
    

    def get_in_edges(self, node: Node) -> dict[Node, list[int]]:
        return {edge: weight for edge, weight in self.graph[node].items() if weight < 0}
    

    def get_out_edges(self, node: Node) -> dict[Node, list[int]]:
        return {edge: weight for edge, weight in self.graph[node].items() if weight > 0}


    def dfs(self, func, node: Node = None) -> Node:  # TODO: add documentation
        if len(self.graph) == 0: return

        visited = set()
        if node is None:
            node = self.graph.keys()[0]
        stack = [node]

        while len(stack):
            i = stack.pop()
            if i not in visited:
                res = func(i)
                if res: return i
                visited.add(i)
                stack.extend(self.graph[i].keys() - visited)


    def bfs(self, func, node: Node = None) -> Node:
        if len(self.graph) == 0: return

        visited = set()
        if node is None:
            node = self.graph.keys()[0]
        queue = [node]

        while len(queue):
            i = queue.pop(0)
            if i not in visited:
                res = func(i)
                if res: return i
                visited.add(i)
                queue.extend(self.graph[i].keys() - visited)

    # TODO: implement Djikstra, A* and other algorithms


class UnweightedDirectedMultiGraph(WeightedDirectedMultiGraph):
    def add_edge(self, node1: WeightedDirectedMultiGraph.Node, node2: WeightedDirectedMultiGraph.Node) -> None:
        super().add_edge(node1, node2, 1)
    

    def remove_edge(self, node1: WeightedDirectedMultiGraph.Node, node2: WeightedDirectedMultiGraph.Node) -> None:
        return super().remove_edge(node1, node2, 1)


class WeightedUndirectedMultiGraph(WeightedDirectedMultiGraph):
    def add_edge(self, node1: WeightedDirectedMultiGraph.Node, node2: WeightedDirectedMultiGraph.Node, weight: int) -> None:
        self.add_node(node1)
        self.add_node(node2)

        if self.graph[node1][node2] is None:
            self.graph[node1][node2] = [weight]
            self.graph[node2][node1] = [weight]
        else:
            self.graph[node1][node2].append(weight)
            self.graph[node2][node1].append(weight)
    

    def remove_edge(self, node1: WeightedDirectedMultiGraph.Node, node2: WeightedDirectedMultiGraph.Node, weight: int) -> None:
        self.graph[node1][node2].remove(weight)
        self.graph[node2][node1].remove(weight)


class UnweightedUndirectedMultiGraph(UnweightedDirectedMultiGraph, WeightedUndirectedMultiGraph):
    pass


class WeightedDirectedSimpleGraph(WeightedDirectedMultiGraph):
    def add_edge(self, node1: WeightedDirectedMultiGraph.Node, node2: WeightedDirectedMultiGraph.Node, weight: int) -> None:
        if node1 is node2: return
        self.graph[node1][node2] = []
        super().add_edge(node1, node2, weight)


    def has_cycle(self) -> bool:
        if len(self.graph) == 0: return False

        visited = set()
        stack = [self.graph.keys()[0]]

        while len(stack):
            node = stack.pop()

            if node in visited: return True

            stack.extend(self.graph[node].keys() - {node})
            visited.add(node)
            
        return False


class WeightedUndirectedSimpleGraph(WeightedDirectedSimpleGraph, WeightedUndirectedMultiGraph):
    pass


class UnweightedDirectedSimpleGraph(WeightedUndirectedSimpleGraph, UnweightedDirectedMultiGraph):
    pass


class UnweightedUndirectedSimpleGraph(WeightedDirectedSimpleGraph, UnweightedUndirectedMultiGraph):
    pass


class MultiGraph(UnweightedDirectedMultiGraph):
    """Unweighted directed simple graph"""


class UndirectedGraph(UnweightedUndirectedSimpleGraph):
    """Unweighted undirected simple graph"""


class WeightedGraph(WeightedDirectedSimpleGraph):
    """Weighted directed simple graph"""


class Graph(UnweightedDirectedSimpleGraph):
    """Unweighted directed simple graph"""
