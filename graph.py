from __future__ import annotations
from typing import TypeVar, Generic

# TODO: Use networkX library instead
# TODO: Simple graph, multigraph
# TODO: Weigted, unweighted

class DirectedGraph:
    class Node:
        def __init__(self, value) -> None:
            self.value = value
            self.edges = set()


        def link(self, other: DirectedGraph.Node) -> None:
            self.edges.add(other)

        
        def unlink(self, other: DirectedGraph.Node) -> None:
            self.edges.discard(other)


    def __init__(self) -> None:
        self.nodes: dict[DirectedGraph.Node, list[DirectedGraph.Node]] = {}
    

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



class UndirectedGraph(DirectedGraph):
    class Node(DirectedGraph.Node):
        def link(self, other: UndirectedGraph.Node) -> None:
            self.edges.add(other)
            other.edges.add(self)
        

        def unlink(self, other: UndirectedGraph.Node) -> None:
            self.edges.discard(other)
            other.edges.discard(self)
        

        def degree(self) -> int:
            return len(self.edges)
