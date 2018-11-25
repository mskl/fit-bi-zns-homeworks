from .term_aggregate import TermAggregate


class Term:
    """ Wrapped up TrapMF that also contains the user input value """

    def __init__(self, membership_function):
        self.membership_function = membership_function

        # User input value
        self.user_input_value = None

    def __getitem__(self, x):
        return self.membership_function[x]

    def __and__(self, other):
        """ movie['Good'] & equipment['Bad'] """
        return TermAggregate(self, other, 'and')

    def __or__(self, other):
        """ movie['Good'] | equipment['Bad'] """
        return TermAggregate(self, other, 'or')

    def __invert__(self):
        """ ~movie['Good'] """
        return TermAggregate(self, None, 'not')

    def evaluate(self):
        """ Evaluate the term based on the user input value """
        if self.user_input_value is None:
            raise ValueError("User input value was not set!")

        return self[self.user_input_value]
