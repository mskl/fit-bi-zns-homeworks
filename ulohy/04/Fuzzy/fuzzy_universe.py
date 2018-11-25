import numpy as np
import matplotlib.pyplot as plt
from Token.tokenized_object import TokenizedObject


class FuzzyUniverse(TokenizedObject):
    """ Fuzzy system universe of one rating parameter """

    def __init__(self, universe_min, universe_max, name):
        """
        :param universe_min: lower limit of the universe
        :param universe_max: upper limit of the universe
        :param name: name to be tokenized
        """
        super().__init__(name)

        # Dict (term_name: term)
        self.terms = dict()
        self.universe_min = universe_min
        self.universe_max = universe_max

    def __getitem__(self, key):
        return self.terms[key]

    def __setitem__(self, key, term):
        self.terms[key] = term

    def set_user_input(self, user_input):
        """ Set the user input to all terms """
        for term_name, term in self.terms.items():
            term.user_input_value = user_input

    def get_plot(self):
        """ Get fig, ax for a matplotlib plot """
        fig, ax = plt.subplots()

        ax.set_ylim([0, 1.05])
        ax.set(title='Fuzzy univerzum -  {}'.format(self.name))

        x_ticks = np.linspace(self.universe_min, self.universe_max, num=11, endpoint=True)
        for key, func in self.terms.items():
            function_values = []
            for x in x_ticks:
                function_values.append(func[x])
            ax.plot(x_ticks, function_values, label=key)

        return fig, ax

    def view(self):
        """ Print a nice looking graph using matplotlib """
        fig, ax = self.get_plot()

        plt.legend(loc='best')
        plt.show()
