import numpy as np
import matplotlib.pyplot as plt

class FuzzySystem:
    """ Fuzzy system contains all information gathered from the expert and the user """

    def __init__(self, rule_list=None, fuzzy_universe_list=None):
        """ Initialise the FuzzySystem with rule array and universes array"""
        if fuzzy_universe_list is None:
            fuzzy_universe_list = []
        if rule_list is None:
            rule_list = []

        # rules are stored in a list
        self.rules = rule_list

        # universes are stored in dict(universe_name: FuzzyUniverse)
        self.fuzzy_universes = dict()
        for universe in fuzzy_universe_list:
            self.add_universe(universe)

        # User inputs dictionary
        self.user_inputs = dict()

    def add_rule(self, rule):
        """ Add a new rule """
        self.rules.append(rule)

    def add_universe(self, universe):
        """ Add a new universe """
        self.fuzzy_universes[universe.name] = universe

    def add_user_input(self, universe_name, value):
        """ Add a new user input and assign it to the universe """
        self.fuzzy_universes[universe_name].set_user_input(value)

    def evaluate_rules(self):
        """
        Evaluate all rules and return rules with non-zero result to the output as a tuple (rule, evaluated value)
        :return: list of tuples (FuzzyRule, evaluated value) with non-zero value
        :rtype: list of (FuzzyRule, float)
        """
        result_rule_list = []

        for rule in self.rules:
            if rule.evaluate() != 0:
                result_rule_list.append((rule, rule.evaluate()))

        return result_rule_list

    def generate_centroid(self, solution_universe, integral_count=10000, show_graph=False):
        """ Calculate the centroid and optionally show the graph """
        centroid = 0
        x = np.linspace(solution_universe.universe_min,solution_universe.universe_max, endpoint=True, num=integral_count)
        y = []

        integral_width = (solution_universe.universe_max - solution_universe.universe_min) / integral_count
        evaluated_rules = self.evaluate_rules()

        def integral_value(_x, _evaluated_rules):
            _y = 0
            for rule, rule_evaluate in _evaluated_rules:
                _y = max(_y, min(rule_evaluate, rule.solution[_x]))
            return _y

        mo = ar = 0
        for _x in x:
            integrated_val_0 = integral_value(_x, evaluated_rules)
            integrated_val_1 = integral_value(_x + integral_width, evaluated_rules)
            y.append(integrated_val_0)

            if (integrated_val_0 != 0) and (integrated_val_1 != 0):
                _ar = integral_width * (integrated_val_0 + integrated_val_1) / 2
                _mo = _x + integral_width / 2

                mo += _mo * _ar
                ar += _ar

        try:
            centroid = mo / ar
        except Exception as ex:
            centroid = 5

        if show_graph:
            fig, ax = solution_universe.get_plot()

            plt.fill_between(x, 0, y, alpha=0.5, color="red")
            plt.plot(x, y, color="black")

            ax.grid()
            plt.axvline(x=centroid, color="black")
            plt.legend(loc='best')
            plt.show()

        return centroid
