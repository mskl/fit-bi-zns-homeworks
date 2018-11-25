from Fuzzy.fuzzy_rule import FuzzyRule
from Token.bag_of_tokens import BagOfTokens


class FuzzyBot:

    def __init__(self):
        self.bag_of_tokens = BagOfTokens()

    def load_knowledge_base(self, knowledge_base_path="znalostni_baze.txt"):
        """
        Load the data from the knowledge base file and parse the clauses.
        """
        with open(knowledge_base_path) as f:
            content = f.readlines()

        for line in content:
            if line.startswith("#"):
                continue

            separated = line.strip(" IF ").split(" THEN ")
            assert (len(separated) == 2)

            conditions = separated[0].split("AND")
            solution = separated[1].split("IS")
            assert (len(solution) == 2)

            solution_name = self.bag_of_tokens.tokenize(solution[0].strip())
            solution_rating = self.bag_of_tokens.tokenize(solution[1].strip())

            for cond in conditions:
                cond = cond.split("IS")
                assert (len(cond) == 2)

                cond_name = self.bag_of_tokens.tokenize(cond[0].strip())
                cond_rating = self.bag_of_tokens.tokenize(cond[1].strip())

                print("{}[{}]".format(cond_name, cond_rating))

            print("-> {}[{}]".format(solution_name, solution_rating))


if __name__ == "__main__":
    fuzzy_bot = FuzzyBot()
    fuzzy_bot.load_knowledge_base()
    print(fuzzy_bot.bag_of_tokens)
