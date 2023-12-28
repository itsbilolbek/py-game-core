from __future__ import annotations
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

# TODO: Use networkX library instead
# TODO: Simple graph, multigraph
# TODO: Weigted, unweighted


class BaseDirectedMultiGraph(ABC):
    pass


class BaseSimpleGraph(BaseDirectedMultiGraph, ABC):
    pass


class BaseDirectedGraph(ABC):
    pass


class BaseUndirectedGraph(BaseDirectedGraph, ABC):
    pass


class BaseWeightedGraph(ABC):
    pass


class BaseUnweightedGraph(BaseWeightedGraph, ABC):
    pass


class WeightedDirectedMultiGraph(BaseDirectedMultiGraph, BaseWeightedGraph):
    # TODO
    pass


class UnweightedDirectedMultiGraph(WeightedDirectedMultiGraph):
    class Node:
        def __init__(self, value) -> None:
            self.value = value
            self.edges = set()


        def link(self, other: UnweightedDirectedMultiGraph.Node) -> None:
            self.edges.add(other)

        
        def unlink(self, other: UnweightedDirectedMultiGraph.Node) -> None:
            self.edges.discard(other)


    def __init__(self) -> None:
        self.nodes: dict[UnweightedDirectedMultiGraph.Node, list[UnweightedDirectedMultiGraph.Node]] = {}
    

    def __getitem__(self, value) -> Node:
        return self.nodes[value]

    
    def add_node(self, node: Node) -> None:
        if node not in self.nodes:
            self.nodes[node] = set()


    def add_nodes(self, nodes: list[Node]) -> None:
        for node in nodes:
            self.add_node(node)
    

    def link_node(self, node1: Node, node2: Node) -> None:
        if node1 not in self.nodes:
            raise

        if node2 not in self.nodes:
            raise

        node1.link(node2)
    

    def unlink_node(self, node1: Node, node2: Node) -> None:
        node1.unlink(node2)



class WeightedUndirectedMultiGraph(WeightedDirectedMultiGraph):
    # TODO
    pass


class UnweightedUndirectedMultiGraph(WeightedUndirectedMultiGraph):
    class Node(UnweightedDirectedMultiGraph.Node):
        def link(self, other: UnweightedUndirectedMultiGraph.Node) -> None:
            self.edges.add(other)
            other.edges.add(self)
        

        def unlink(self, other: UnweightedUndirectedMultiGraph.Node) -> None:
            self.edges.discard(other)
            other.edges.discard(self)
        

        def degree(self) -> int:
            return len(self.edges)


class WeightedDirectedSimpleGraph(WeightedDirectedMultiGraph):
    # TODO
    pass


class WeightedUndirectedSimpleGraph(WeightedUndirectedMultiGraph):
    # TODO
    pass


class UnweightedDirectedSimpleGraph(UnweightedDirectedMultiGraph):
    # TODO
    pass


class UnweightedUndirectedSimpleGraph(UnweightedUndirectedMultiGraph):
    # TODO
    pass


class SimpleGraph(UnweightedDirectedSimpleGraph):
    """Unweighted directed simple graph"""


class UndirectedGraph(UnweightedUndirectedMultiGraph):
    """Unweighted undirected multi graph"""


class WeightedGraph(WeightedDirectedMultiGraph):
    """Weighted directed multigraph"""


class Graph(UnweightedDirectedMultiGraph):
    """Unweighted directed multi graph"""
