from __future__ import annotations
from typing import TypeVar, Generic
from abc import ABC, abstractmethod


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


class WeightedUndirectedSimpleGraph(WeightedDirectedSimpleGraph, WeightedUndirectedMultiGraph):
    pass


class UnweightedDirectedSimpleGraph(WeightedUndirectedSimpleGraph, UnweightedDirectedMultiGraph):
    pass


class UnweightedUndirectedSimpleGraph(WeightedDirectedSimpleGraph, UnweightedUndirectedMultiGraph):
    pass


class SimpleGraph(UnweightedDirectedSimpleGraph):
    """Unweighted directed simple graph"""


class UndirectedGraph(UnweightedUndirectedMultiGraph):
    """Unweighted undirected multi graph"""


class WeightedGraph(WeightedDirectedMultiGraph):
    """Weighted directed multigraph"""


class Graph(UnweightedDirectedMultiGraph):
    """Unweighted directed multi graph"""
