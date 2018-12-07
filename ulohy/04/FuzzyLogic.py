from Fuzzy import FuzzyUniverse, FuzzyRule, FuzzySystem
import Fuzzy.Function as Function
from Fuzzy.Term import Term
from FuzzyRuleset import FuzzyRuleset
import sys


class ChatBot:
    def __init__(self):
        self.fuzzy_ruleset = FuzzyRuleset()

        self.universes = list(self.fuzzy_ruleset.fuzzy_system.fuzzy_universes.items())
        self.ratings = []
        self.current = 0
        self.max = len(self.universes) - 1

        self.user_input = True
        if len(sys.argv) == 2:
            self.user_input = False
            self.lines = open(sys.argv[1]).read().splitlines()

    def _post_question(self, question):
        if self.user_input:
            return input(question)
        else:
            ans = self.lines.pop(0)
            print(question + ans)
            return ans

    def _post_answer(self, answer):
        print(answer)

    def ask(self):
        response = self._post_question("Jak hodnotíš \"" + self.universes[self.current][0] + "\"? [s/<0, 10>]: ")

        # Check for numerical response
        response_num = None
        if response == "s":
            pass
        else:
            try:
                response_num = float(response)

                if not (0 <= response_num <= 10):
                    self._post_answer("*Zadané číslo není z intervalu <0, 10>.")
                    return False
            except ValueError:
                self._post_answer("*Neznámá odpověď.")
                return False

        """ Actions based on the response of the user: """
        if response_num is not None:
            self.universes[self.current][1].set_user_input(response_num)
            self.current += 1
            if self.current >= self.max:
                result = self.fuzzy_ruleset.evaluate(show_graph=False)
                if "y" == self._post_question("*Výsledné hodnocení: %.2f. Chceš vědět proč? [y/*]: " % result):
                    self.fuzzy_ruleset.evaluate(show_graph=True)
                return True

        elif response == "s":
            self.universes[self.current][1].view()

        else:
            self._post_answer("*Neznámá odpověď.")

        return False


if __name__ == "__main__":
    print("*Fuzzy systém pro hodnocení závodů OB nastartován.")
    c = None

    try:
        c = ChatBot()
    except Exception as e:
        print("*Inicialization of the chatbot failed with the error of:", str(e))
        exit(0)

    while not c.ask():
        pass

    print("*Konec programu.")
