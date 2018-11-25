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

    def generate_centroid(self, solution_universe, integral_count=1000, show_graph=False):
        """ Calculate the centroid and optionally show the graph """
        function_points = np.linspace(solution_universe.universe_min,
                                      solution_universe.universe_max,
                                      endpoint=True, num=integral_count)
        centroid = 0
        function_results = []

        evaluated_rules = self.evaluate_rules()
        for p in function_points:
            max_function_value = 0
            for rule, rule_evaluate in evaluated_rules:
                max_function_value = max(max_function_value, min(rule_evaluate, rule.solution[p]))
            centroid += max_function_value * p
            function_results.append(max_function_value)

        centroid /= integral_count / 2

        if show_graph:
            fig, ax = solution_universe.get_plot()
            ax.plot(function_points, function_results)
            plt.fill(function_points, function_results, alpha=0.5, color="red")
            ax.grid()
            plt.axvline(x=centroid, color="black")
            plt.legend(loc='best')
            plt.show()

        return centroid
