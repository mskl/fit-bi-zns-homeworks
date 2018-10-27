class Node:
    edges = set()
    name = ""
    value = None
    __id = None

    def __init__(self, id, name="Unnamed node"):
        self.edges = set()
        self.name = name
        self.__id = id

        self.value = None

    def get_id(self):
        return self.__id

    def add_edge(self, edge):
        self.edges.add(edge)

    def __id__(self):
        return "id=" + str(self.__id) + " name=\"" + str(self.name)

    def __str__(self):
        return self.__id__() + "\" edges=" + str(len(self.edges))

    def __eq__(self, other):
        if other is None:
            return False
        elif hash(self) == hash(other):
            return True
        return False

    def __hash__(self):
        return hash(self.__id__())
