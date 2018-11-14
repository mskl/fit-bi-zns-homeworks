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

    def calculate_max_heights(self):
        """
        Calculate the maximum distance to a leaf that the node has.
        """
        for i in self.nodes:
            i.calculate_height()

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

    def get_node(self, node, create=True):
        """
        Get a node from the given string.
        :param node: node or name of the node
        :param create: node should be created if missing
        :type node: Node | str
        :type create: bool
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
            if create:
                return self.__add_node(node)
            else:
                raise ValueError("Creation blocked.")
        else:
            raise KeyError("Unknown node type")

    def get_subgraph(self, node):
        """
        Get a set of nodes that are in the same subgraph as the current node.
        :param node: node that needs to be searched
        :type node: Node | str
        :return: set of the nodes in the same subgraph
        :rtype: set of Node
        """
        # get the node from the name
        node = self.get_node(node, create=False)

        visited = set()
        unvisited = set()

        # add the starting node
        unvisited.add(node)

        while unvisited:
            n = unvisited.pop()
            visited.add(n)
            for e_o in n.edges_out:
                o = e_o.other(n)
                if o not in visited:
                    unvisited.add(o)
            for e_i in n.edges_in:
                i = e_i.other(n)
                if i not in visited:
                    unvisited.add(i)

        return visited

    def remove_nodes(self, nodes):
        """
        Removes all given nodes from graph and their edges.
        :param nodes: iterable collection of nodes
        :type nodes: set
        """
        to_remove = []
        for n in nodes:
            to_remove.append(n)
        for n in to_remove:
            self.remove_node(n)

    def remove_node(self, node):
        """
        Remove node and all affected edges.
        :param node: Node to be deleted. Either node or a string
        """
        # find the node if passed a string
        node = self.get_node(node, create=False)

        for e in node.edges_in:
            other_node = e.other(node)
            other_node.remove_edges_containing(node)

        for e in node.edges_out:
            other_node = e.other(node)
            other_node.remove_edges_containing(node)

        node.remove_edges_containing(node)

        # remove global node and delete the object
        self.nodes.remove(node)

    def remove_ancestor_branch(self, node):
        """
        Recursively remove ancestors on a branch if they have only one output.
        :type node: Node | str
        """
        node = self.get_node(node, create=False)

        if len(node.edges_out) == 1:
            ancestors = []
            for e_in in node.edges_in:
                other_node = e_in.other(node)
                ancestors.append(other_node)
            for n in ancestors:
                self.remove_ancestor_branch(n)
            self.remove_node(node)

    def remove_node_and_descendants(self, node, ancestors, direct, node_from=None, user_prob=None):
        """
        Recursively delete the node and it's descendants if they have only one input.
        :param direct: remove only direct branch
        :param user_prob: probability given by the user (or 1)
        :param node: node or name of a node
        :param node_from: previous node
        :param ancestors: true to remove the single ancestor branch
        :type node: Node
        """
        node = self.get_node(node)

        other_nodes = []
        for e in node.edges_out:
            other_node = e.other(node)

            if user_prob is not None:
                other_node.add_L(p_e=node.p, p_he=e.get_value(), user_prob=user_prob)

            # solve if middle node or last
            if len(other_node.edges_in) == 1:
                other_node.p = other_node.ziskej_finalni_pst()
                other_node.calculated = True

            if direct:
                # remove only if it has 1 input, else it might be useful
                if len(other_node.edges_in) == 1:
                    other_nodes.append(other_node)
            else:
                other_nodes.append(other_node)

        for n in other_nodes:
            self.remove_node_and_descendants(n, ancestors, direct, node)

        # remove also the unsolvable branches up
        # no need to recalculate probability
        if ancestors:
            ancestor_nodes = []
            for i in node.edges_in:
                if not i.contains(node_from):
                    ancestor_nodes.append(i.other(node))
            for n in ancestor_nodes:
                self.remove_ancestor_branch(n)

        self.remove_node(node)

    # Add an edge either from two nodes of from two strings
    def add_edge(self, id_a, id_b, value="", a_value=None, b_value=None):
        """
        Adds an edge and automatically creates a node if it does not exist.
        :param id_a: Node or name of a new node (source)
        :param id_b: Node or name of a new node (destination)
        :param value: Value of the edge
        :param b_value: value to be assigned to node a
        :param a_value: value to be assigned to node b
        """
        a = self.get_node(id_a)
        b = self.get_node(id_b)

        # update the values of nodes if given
        if a_value is not None:
            a.p = a_value
        if b_value is not None:
            b.p = b_value

        # Create a new edge
        new_edge = Edge(a, b, self.__creation_edge_counter, value)
        self.__creation_edge_counter = self.__creation_edge_counter + 1

        # Add the edge to both nodes
        a.edges_out.add(new_edge)
        b.edges_in.add(new_edge)

    def graphviz_draw(self, preview=True, name="znalostni_baze"):
        """
        Draw the graph using the Graphviz graphing library.
        :param name: name of the generated file and graph
        :param preview: Show the generated graph.
        :type preview: bool
        """
        dot = Digraph(comment=self.name, format="pdf")
        for node in self.nodes:
            dot.node(str(node.get_id()), str(node.name), _attributes={"xlabel": node.get_value_string()})
            for edge in node.edges_out:
                other_node = edge.other(node)
                dot.edge(str(node.get_id()), str(other_node.get_id()), str(edge.get_value()))

        # print(dot.source)
        apply_styles(dot, graph_style)
        dot.render(name, view=preview, cleanup=True)

    def print_nice(self):
        """
        Nicely print the graph.
        """
        self.nodes = sorted(self.nodes, key=(lambda x: (x.height, len(x.edges_out))), reverse=True)
        for v in self.nodes:
            for e in v.edges_out:
                e.print_nice()

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
