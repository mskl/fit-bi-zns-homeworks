class TermAggregate:
    """ Used to store combinations of Terms """

    def __init__(self, term1, term2, kind):
        """ Note that func2 might be None in case of inverse """
        self.func1 = term1
        self.func2 = term2
        self.kind = kind

    def __getitem__(self, x):
        """ Evaluate the function in any given point x """
        # x ∧ y → min(x, y)
        if self.kind == "and":
            return min(self.func1[x], self.func2[x])

        # x ∨ y → max(x, y)
        if self.kind == "or":
            return max(self.func1[x], self.func2[x])

        # ¬x → 1 − µ(x)
        if self.kind == "not":
            return 1 - self.func1[x]

        raise ValueError("Unknown kind of aggregation.")

    def evaluate(self):
        """ Evaluate the term aggregate based on the user input value """
        # x ∧ y → min(x, y)
        if self.kind == "and":
            return min(self.func1.evaluate(), self.func2.evaluate())

        # x ∨ y → max(x, y)
        if self.kind == "or":
            return max(self.func1.evaluate(), self.func2.evaluate())

        # ¬x → 1 − µ(x)
        if self.kind == "not":
            return 1 - self.func1.evaluate()

        raise ValueError("Unknown kind of aggregation.")
