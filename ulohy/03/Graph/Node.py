class Node:
    def __init__(self, id, name="Unnamed node"):
        """
        Generate a new node.
        :param id: unique id
        :type id: int
        :param name: name of the node
        :type name: str
        """
        self.__id = id
        self.edges_out = set()
        self.edges_in = set()
        self.height = 0
        self.name = name

        # bayes system variables
        self.p = None      # probability
        self.Ls_ = []   # Array of L'

    def O(self, p):
        return p / (1 - p)

    def P(self, o):
        return o / (1 + o)

    def L_(self, p_he_, p_h):
        return self.O(p_he_) / self.O(p_h)

    def add_L(self, p_e, p_he, user_prob):
        p_h = self.p
        p_eh = self.P_HE_(p_e=p_e, p_h=self.p, p_he=p_he, user_prob=user_prob)
        self.Ls_.append(self.L_(p_eh, p_h=p_h))

    def nasobek_sanci(self, p_h, sance_):
        o_h = self.O(p_h)
        for s in sance_:
            o_h *= s
        return o_h

    def ziskej_finalni_pst(self):
        return self.P(self.nasobek_sanci(self.p, self.Ls_))

    def P_HE_(self, p_e, p_h, p_he, user_prob):
        """
        returns: p_he_
        """
        p_hxe = 0

        if 0 <= user_prob <= p_e:
            return p_hxe + ((p_h - p_hxe) / p_e) * user_prob
        elif p_e <= user_prob <= 1:
            return p_h + ((p_he - p_h) / (1 - p_e)) * (user_prob - p_e)
        else:
            raise ValueError("p_ee_ is out of range")

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

    def calculate_height(self):
        """
        Recursively calculate the maximum distance to any leaf.
        :return: height value
        :rtype: int
        """
        for e in self.edges_out:
            n = e.other(self)
            self.height = max(n.calculate_height(), self.height)
        return self.height + 1

    def get_solution(self):
        """
        Recursively find any (only) leaf.
        :rtype: Node
        :return: any leaf
        """
        if len(self.edges_out) > 1 or len(self.edges_in) > 1:
            return None
        for e in self.edges_out:
            return e.other(self).get_solution()
        return self

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

    def get_value_string(self):
        """
        Get the value of the node in a string format.
        :rtype: str
        :return: node value
        """
        rstring = ""
        if self.p is not None:
            rstring += "p: " + str(self.p)
        if len(self.Ls_) != 0:
            if rstring is not None:
                rstring += " | "
            rstring += "Ls_: "
            for i in self.Ls_:
                rstring += str(i) + ", "
        rstring += " | calculated: " + str(self.ziskej_finalni_pst())
        return rstring

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
