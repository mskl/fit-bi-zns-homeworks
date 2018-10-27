from graphviz import Digraph
from Graph.Node import Node
from Graph.Edge import Edge
from Graph.GraphvizStyles import *


class Graph:
    def __init__(self, name="Unnamed graph"):
        self.name = name
        self.nodes = set()
        self.edges = set()
        self.__creation_node_counter = 0
        self.__creation_edge_counter = 0

    # Add a named node. The ID is generated automatically.
    def __add_node(self, name):
        new_node = Node(self.__creation_node_counter, name)
        self.nodes.add(new_node)
        self.__creation_node_counter = self.__creation_node_counter + 1
        return new_node

    def __remove_edge(self, edge):
        self.edges.remove(edge)

    def remove_node(self, node):
        # find the node if passed a string
        if isinstance(node, str):
            for v in self.nodes:
                if v.name == node:
                    node = v
                    break

        if not isinstance(node, Node):
            raise TypeError()

        # edges to be removed
        for e in node.edges:
            other_node = e.other(node)

            # find the edge in other node
            for o in other_node.edges:
                if o.any() == e or o.other(o.any()) == e:
                    other_node.edges.remove(o)
                    break

        if node not in self.nodes:
            raise KeyError()
        else:
            self.nodes.remove(node)
            del node

    def remove_node_and_descendants(self, node):
        pass

    # Add an edge either from two nodes of from two strings
    def add_edge(self, id_a, id_b, value=""):
        a = b = None

        if isinstance(id_a, Node) and isinstance(id_b, Node):
            for v in self.nodes:
                if v == id_a:
                    a = v
                elif v == id_b:
                    b = v
                if a is not None and b is not None:
                    break
        elif isinstance(id_a, str) and isinstance(id_b, str):
            for v in self.nodes:
                if v.name == id_a:
                    a = v
                elif v.name == id_b:
                    b = v
                if a is not None and b is not None:
                    break
        else:
            return

        # One of the instances is neither a node or a string
        if a is None:
            if isinstance(id_a, Node):
                self.nodes.add(id_a)
            else:
                a = self.__add_node(id_a)
        if b is None:
            if isinstance(id_b, Node):
                self.nodes.add(id_b)
            else:
                b = self.__add_node(id_b)

        # Create a new edge
        new_edge = Edge(a, b, self.__creation_edge_counter, value)
        self.__creation_edge_counter = self.__creation_edge_counter + 1

        b.edges.add(new_edge)           # the other node WARNING was a.add_edge!
        self.edges.add(new_edge)        # this node

    def graphviz_draw(self, view=True):
        # Create a new graph
        dot = Digraph(comment=self.name, format="pdf")

        # Draw all nodes
        for v in self.nodes:
            dot.node(str(v.get_id()), str(v.name))

            for e in v.edges:
                other = e.other(v)
                dot.edge(str(other.get_id()), str(v.get_id()), str(e.get_value()))

        # Print the text structure
        # print(dot.source)

        # Apply the styles
        apply_styles(dot, graph_style)

        # Render the final graph
        dot.render('image_output/%s' % self.name, view=view)

    def __str__(self):
        s = ("========== " + str(self.name) + " ==========\n")
        for v in self.nodes:
            s += str(v) + "\n"
            for e in v.edges:
                s += ("--- " + str(e) + "\n")
        return s
