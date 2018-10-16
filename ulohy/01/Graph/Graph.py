from graphviz import Digraph
from Graph.Node import Node
from Graph.Edge import Edge
from Graph.GraphvizStyles import *


class Graph:
    def __init__(self, name="Unnamed graph"):
        self.__name = name
        self.__nodes = []
        self.__edges = []

    # Add a named node. The ID is generated automatically.
    def add_node(self, name):
            self.__nodes.append(Node(name))

    # Add an edge either from two nodes of from two strings
    def add_edge(self, id_a, id_b, value="unknown", bidirectional=False):
        a = b = None

        if isinstance(id_a, Node) and isinstance(id_b, Node):
            # Iterate and search for vertices with id
            for v in self.__nodes:
                if v.get_id() == id_a:
                    a = v
                elif v.get_id() == id_b:
                    b = v
                elif a is not None and b is not None: break
        elif isinstance(id_a, str) and isinstance(id_b, str):
            # Iterate and search for vertices with name
            for v in self.__nodes:
                if v.get_name() == id_a:
                    a = v
                elif v.get_name() == id_b:
                    b = v
                elif a is not None and b is not None: break
        else: return

        # If none was found assign nothing
        if a is None:
            if isinstance(id_a, Node):
                self.__nodes.append(a)
            else:
                a = Node(id_a)
                self.__nodes.append(a)
        if b is None:
            if isinstance(id_b, Node):
                self.__nodes.append(b)
            else:
                b = Node(id_b)
                self.__nodes.append(b)

        # Create a new edge
        new_edge = Edge(a, b, value)

        # Append it to a node and to the list as well
        a.add_edge(new_edge)
        self.__edges.append(new_edge)

        # If the edge is bidirectional add the other edge as well
        if bidirectional:
            b.add_edge(new_edge)

    def graphviz_draw(self, view=True):
        # Create a new graph
        dot = Digraph(comment=self.__name, format="pdf")

        # Draw all nodes
        for v in self.__nodes:
            dot.node(str(v.get_id()), str(v.get_name()))

            for e in v.get_edges():
                other = e.other(v)
                dot.edge(str(other.get_id()), str(v.get_id()), str(e.get_value()))

        # Print the text structure
        print(dot.source)

        # Apply the styles
        apply_styles(dot, graph_style)

        # Render the final graph
        dot.render('image_output/%s' % self.__name, view=view)

    def __str__(self):
        s = ("========== " + str(self.__name) + " ==========\n")
        for v in self.__nodes:
            s += str(v) + "\n"
            for e in self.__edges:
                s += ("--- " + str(e) + "\n")
        return s
