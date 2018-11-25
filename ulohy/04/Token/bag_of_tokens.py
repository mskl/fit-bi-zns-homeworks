from Token.tokenized_object import TokenizedObject


class BagOfTokens:
    def __init__(self):
        self.tokens = set()

    def tokenize(self, token_name) -> TokenizedObject:
        temporary_term = TokenizedObject(token_name)

        if token_name not in self.tokens:
            self.tokens.add(temporary_term)

        return temporary_term

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        r_string = "Bag of tokens ["
        for i in self.tokens:
            r_string += str(i) + ", "
        return r_string.rstrip(", ") + "]"


if __name__ == "__main__":
    bag = BagOfTokens()
    bag.tokenize("ahoj")
    bag.tokenize("vole")
    bag.tokenize("ahoj")
    print(bag)
