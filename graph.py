class WeightedDirectedMultiGraph:
    class Node:
        def __init__(self, value) -> None:
            self.value = value


    def __init__(self) -> None:
        self.graph: dict[self.Node, dict[self.Node, list[int]]] = {}

    
    def add_node(self, node: Node) -> None:
        if node not in self.graph:
            self.graph[node] = {}
    

    def remove_node(self, node: Node) -> None:
        for other, edges in self.graph[node].items():
            for weight in edges:
                self.remove_edge(node, other, weight)
        
        self.graph.pop(node)
    

    def find_node(self, node: Node) -> bool:
        for i in self.graph:
            if i is node:
                return True
        
        return False
    

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


    def dfs(self, func, node: Node = None) -> None:
        if len(self.graph) == 0: return

        visited = set()
        if node is None:
            node = self.graph.keys()[0]
        stack = [node]

        while len(stack):
            i = stack.pop()
            if i not in visited:
                visited.add(i)
                stack.extend(self.graph[i].keys() - visited)
                if func(i): return


    def bfs(self, func, node: Node = None) -> None:
        if len(self.graph) == 0: return

        visited = set()
        if node is None:
            node = self.graph.keys()[0]
        queue = [node]

        while len(queue):
            i = queue.pop(0)
            if i not in visited:
                visited.add(i)
                queue.extend(self.graph[i].keys() - visited)
                if func(i): return

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
    """Unweighted undirected multi graph"""


class WeightedGraph(WeightedDirectedSimpleGraph):
    """Weighted directed multigraph"""


class Graph(UnweightedDirectedSimpleGraph):
    """Unweighted directed multi graph"""
