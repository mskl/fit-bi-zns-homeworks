from graphviz import Digraph
from Graph.Node import Node
from Graph.Edge import Edge
from Graph.GraphvizStyles import *


class Graph:
    def __init__(self, name="Unnamed graph"):
        """
        Create a new graph give a name.
        :param name: name of the graph
        :type name: str
        """
        self.name = name
        self.nodes = set()
        self.__creation_node_counter = 0
        self.__creation_edge_counter = 0

    def __add_node(self, name):
        """
        Adds a node. The id is generated automatically.
        :param name: name of the node
        :rtype: Node
        """
        new_node = Node(self.__creation_node_counter, name)
        self.nodes.add(new_node)
        self.__creation_node_counter = self.__creation_node_counter + 1
        return new_node

    def get_node(self, node):
        """
        Get a node from the given string.
        :param node: node or name of the node
        :type node: Node | str
        :return: a new node if it does not exist
        :rtype Node
        """
        if isinstance(node, Node):
            self.nodes.add(node)
            return node
        elif isinstance(node, str):
            for v in self.nodes:
                if v.name == node:
                    return v
            return self.__add_node(node)
        else:
            raise KeyError("Unknown node type")

    def remove_node(self, node):
        """
        Remove node and all affected edges.
        :param node: Node to be deleted. Either node or a string
        """
        # find the node if passed a string
        node = self.get_node(node)

        for e in node.edges_in:
            other_node = e.other(node)
            other_node.remove_edges_containing(node)

        for e in node.edges_out:
            other_node = e.other(node)
            other_node.remove_edges_containing(node)

        node.remove_edges_containing(node)

        # remove global node and delete the object
        self.nodes.remove(node)
        del node

    def remove_node_and_descendants(self, node):
        """
        Recursively delete the node and it's descendants.
        :param node: node or name of a node
        :return:
        """
        if isinstance(node, str):
            node = self.get_node(node)

        other_nodes = []
        for e in node.edges_out:
            other_nodes.append(e.other(node))

        for n in other_nodes:
            self.remove_node_and_descendants(n)

        self.remove_node(node)

    # Add an edge either from two nodes of from two strings
    def add_edge(self, id_a, id_b, value=""):
        """
        Adds an edge and automatically creates a node if it does not exist.
        :param id_a: Node or name of a new node (source)
        :param id_b: Node or name of a new node (destination)
        :param value: Value of the edge
        """
        a = self.get_node(id_a)
        b = self.get_node(id_b)

        # Create a new edge
        new_edge = Edge(a, b, self.__creation_edge_counter, value)
        self.__creation_edge_counter = self.__creation_edge_counter + 1

        # Add the edge to both nodes
        a.edges_out.add(new_edge)
        b.edges_in.add(new_edge)

    def graphviz_draw(self, view=True):
        """
        Draw the graph using the Graphviz graphing library.
        :param view: Show the generated graph.
        :type view: bool
        """
        dot = Digraph(comment=self.name, format="pdf")
        for node in self.nodes:
            dot.node(str(node.get_id()), str(node.name))
            for edge in node.edges_out:
                other_node = edge.other(node)
                dot.edge(str(node.get_id()), str(other_node.get_id()), str(edge.get_value()))

        print(dot.source)
        apply_styles(dot, graph_style)
        dot.render('image_output/%s' % self.name, view=view)

    def __str__(self):
        """
        Graph representation used for debugging.
        :rtype: str
        """
        s = ("========== " + str(self.name) + " ==========\n")
        for v in self.nodes:
            s += str(v) + "\n"
            for e in v.edges_in:
                s += ("--> " + str(e) + "\n")
            for e in v.edges_out:
                s += ("<-- " + str(e) + "\n")
        return s
