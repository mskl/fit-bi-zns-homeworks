class FuzzyRule:
    """ Contains the conditions and a solution"""

    def __init__(self, conditions, solution):
        """
        Rule contains the conditions and a solution
        :type conditions: Term | TermAggregate
        :type solution: Term
        """
        self.conditions = conditions
        self.solution = solution

    def evaluate(self):
        """
        Evaluate the whole fuzzy rule
        :rtype: (float, Term | TermAggregate)
        """
        return self.conditions.evaluate()
