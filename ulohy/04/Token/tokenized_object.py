
class TokenizedObject(object):
    """
    Crate a new unique object for each keyword
    """

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return str(id(self)) + "[" + self.name + "]"
