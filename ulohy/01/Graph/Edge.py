class Edge:
    def __init__(self, node_a, node_b, edge_value = "null"):
        self.__node_a = node_a
        self.__node_b = node_b
        self.__edge_value = edge_value

    def any(self):
        return self.__node_a

    def other(self, node):
        if node == self.__node_a:
            return self.__node_b
        elif node == self.__node_b:
            return self.__node_a
        return None

    def get_value(self):
        return self.__edge_value

    def __str__(self):
        return "a: " + str(self.__node_a) + " || b: " + str(self.__node_b) + " || value=" + str(self.__edge_value)

    def __eq__(self, other):
        if self.any() == other.any():
            if self.other(self.any()) == other.other(other.any()):
                return True
        elif self.any() == other.other(other.any()):
            if self.other(self.any()) == other.any():
                return True
        return False
