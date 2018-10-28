class Node:
    def __init__(self, id, name="Unnamed node"):
        """
        Generate a new node.
        :param id: unique id
        :type id: int
        :param name: name of the node
        :type name: str
        """
        self.edges_out = set()
        self.edges_in = set()
        self.value = None
        self.name = name
        self.__id = id

    def remove_edges_containing(self, node):
        """
        Remove all edges on this node that contain the node from the parameter.
        :param node: the node that needs to be removed
        :type node: Node
        """
        # remove incoming
        to_remove_in = []
        for e in self.edges_in:
            if e.contains(node):
                to_remove_in.append(e)
        for d in to_remove_in:
            self.edges_in.remove(d)

        # remove outgoing
        to_remove_out = []
        for e in self.edges_out:
            if e.contains(node):
                to_remove_out.append(e)
        for d in to_remove_out:
            self.edges_out.remove(d)

    def __id__(self):
        """
        Unique id of the Node used for hashing
        :rtype: str
        """
        return "id=" + str(self.__id) + " name=\"" + str(self.name)

    def get_id(self):
        """
        Get the unique id assigned when creating.
        :return: unique creation id
        :rtype: int
        """
        return self.__id

    def __str__(self):
        """
        String representation of the node.
        :return: string representation of the node.
        """
        return self.__id__() + "\" e_in=" + str(len(self.edges_in)) + " e_out=" + str(len(self.edges_out))

    def __eq__(self, other):
        """
        Check if 2 node are equal by comparing their hashes.
        :param other: other node
        :type other: Node
        :rtype: bool
        """
        if other is None:
            return False
        elif hash(self) == hash(other):
            return True
        return False

    def __hash__(self):
        """
        Unique hash generated from the id string.
        :return: unique hash
        """
        return hash(self.__id__())
