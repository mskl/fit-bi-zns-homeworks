class Edge:
    def __init__(self, node_a, node_b, id, edge_value="null"):
        """
        Create a new edge using an unique id and a edge value.
        :type node_a: Node
        :type node_b: Node
        :param id: unique id
        :type id: int
        :param edge_value: value of the edge
        """
        self.__node_a = node_a
        self.__node_b = node_b
        self.__edge_value = edge_value
        self.__id = id

    def any(self):
        """
        Return any node of the edge.
        :rtype: Node
        """
        return self.__node_a

    def other(self, node):
        """
        Return the other node on the edge.
        :param node: the other node
        :type node: Node
        :rtype: Node
        """
        if node == self.__node_a:
            return self.__node_b
        elif node == self.__node_b:
            return self.__node_a

    def from_node(self, a):
        """
        Checks if the edge leads from the node.
        :param a: source node
        :type a: Node
        :rtype: bool
        """
        return a == self.__node_a

    def to_node(self, b):
        """
        Checks if the edge leads to the node.
        :param b: dest node
        :type b: Node
        :rtype: bool
        """
        return b == self.__node_b

    def contains(self, node):
        """
        Check if the edge contains a node.
        :type node: Node
        :rtype: bool
        """
        return node == self.__node_a or node == self.__node_b

    def get_value(self):
        """
        Return the value of the edge.
        :return: edge value
        """
        return self.__edge_value

    def __id__(self):
        """
        Get an unique id for hashing.
        :return: unique id string
        :rtype: str
        """
        return "e_id=" + str(self.__id) + " e_value=" + str(self.__edge_value)

    def print_nice(self):
        """
        Nicely print the current edge.
        """
        print("- " + str(self.__node_a.name) + " -> " + str(self.__node_b.name))

    def __str__(self):
        """
        Describe the current edge.
        :return: edge description
        :rtype: str
        """
        return self.__id__() + " || " + str(self.__node_a.name) + " -> " + str(self.__node_b.name)

    def __eq__(self, other):
        """
        Check if 2 edges are equal
        :param other: other edge
        :type other: Edge
        :rtype: bool
        """
        if self.any() == other.any():
            if self.other(self.any()) == other.other(other.any()):
                return True
        elif self.any() == other.other(other.any()):
            if self.other(self.any()) == other.any():
                return True
        return False

    def __hash__(self):
        """
        Unique hash generated from the id string.
        :return: hash
        """
        return hash(str(self.__id__))