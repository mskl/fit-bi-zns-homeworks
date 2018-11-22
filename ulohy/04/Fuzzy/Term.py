class Term:

    def __init__(self, name="unknown"):
        self.name = name

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)