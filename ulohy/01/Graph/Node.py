class Node:
    creation_id_counter = 0

    def __init__(self, name="Unnamed node"):
        self.__edges = []
        self.__name = name
        self.__id = self.creation_id_counter

        # Update the id creation id counter
        Node.creation_id_counter = Node.creation_id_counter + 1

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_edges(self):
        return self.__edges

    def add_edge(self, edge):
        self.__edges.append(edge)

    def __str__(self):
        return "id=" + str(self.__id) + " name=\"" + str(self.__name) + "\" edges=" + str(len(self.__edges))

    def __eq__(self, other):
        if other is None:
            return False
        elif self.__id == other.__id:
            return True
        return False

    def set_diamond_attr(self):
        self.graphviz_attributes['nodes']['shape'] = 'egg'
