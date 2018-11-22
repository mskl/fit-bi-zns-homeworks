from Term import Term

class BagOfTerms:
    def __init__(self):
        self.terms = set() # set of Literal objects

    def add_term(self, term):
        """
        Tokenize the term
        :param term: the term to be tokenized
        :type term: String
        :return: tokenized Term
        """

        temporary_term = Term(term)

        if term not in self.terms:
            # create a new term and add it to the hashset
            self.terms.add(temporary_term)

        return temporary_term

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        r_string = "Bag of terms ["
        for i in self.terms:
            r_string += str(i) + ", "
        return r_string.rstrip(", ") + "]"


if __name__ == "__main__":
    bag = BagOfTerms()
    bag.add_term("ahoj")
    bag.add_term("vole")
    bag.add_term("ahoj")
    print(bag)