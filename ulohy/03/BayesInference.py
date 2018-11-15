from Graph.Graph import Graph
import sys


class ChatBot:
    def __init__(self):
        """
        Load the data and calculate the heights.
        """
        self.data_graph = self._initialise_data()

        self.messages_sent = []
        self.messages_received = []

        self.answered_true = set()
        self.implied_true = set()

        self.current_subgraph = set()

        self.explanations = []

        self.user_input = True
        if len(sys.argv) == 2:
            self.user_input = False
            self.lines = open(sys.argv[1]).read().splitlines()

    def _load_data(self):
        """
        Load the data from the knowledge base file and parse the clauses.
        """
        with open("znalostni_baze.txt") as f:
            content = f.readlines()

        data_graph = Graph("Expertní systém opraváře kol")
        for line in content:
            if line.startswith("#"):
                continue
            separated = line.strip(" IF ").split(" THEN ")
            if len(separated) == 2:
                conditions = separated[0].split("AND")
                solution_name = separated[1].split("|")[0]
                p_h = float(separated[1].split("|")[1].strip("\n "))
                for cond in conditions:
                    cond_name = cond.split("|")[0]
                    probabilities = cond.split("|")[1].split("->")
                    p_e = float(probabilities[0])
                    p_he = float(probabilities[1])

                    data_graph.add_edge(cond_name.strip(), solution_name.strip(), value=p_he, a_value=p_e, b_value=p_h)
        return data_graph

    def _initialise_data(self):
        """
        Load the data and calculate heights.
        :return: initialised graph with heights set
        """
        data_graph = self._load_data()
        data_graph.calculate_max_heights()
        return data_graph

    def _select_sources(self, nodes):
        """
        Create a list of pairs (input edge count, node) that is sorted from highest count.
        :param nodes: nodes to be processed
        :rtype: list of Node
        :return: sorted list of int, node
        """
        node_sources = []
        for node in nodes:
            if len(node.edges_in) == 0:
                node_sources.append(node)

        node_sources.sort(reverse=True, key=lambda n: (len(n.edges_out), n.height, n.name))
        return node_sources

    def _post_question(self, question):
        """
        Post a question and wait for the user's response.
        :param question: question to be asked
        :type question: str
        :return: response to the question
        :rtype: str
        """
        self.messages_sent.append(question)
        if self.user_input:
            return input(question)
        else:
            ans = self.lines.pop(0)
            print(question + ans)
            return ans

    def _post_answer(self, answer):
        """
        Post an answer to the user and save it for analysis.
        :param answer: answer to be shown to the user
        """
        print(answer)
        self.messages_received.append(answer)

    def _why(self, current_data):
        """
        Tell the user why I'm asking him this question.
        """
        if len(self.answered_true) > 0:
            print("*Uživatel odpověděl pravdivě na následující otázky: ")
            for i in self.answered_true:
                print("---", i.name)
        if len(self.implied_true) > 0:
            print("*Z nich vyplývá, že: ")
            for i in self.implied_true:
                print("---", i.name)
        print("*Jsou celkem {} otázky, které mohou pomoci posunout se dál. Top {} z nich jsou: " \
              .format(len(current_data), min(len(current_data), 3)))
        for n in range(0, min(len(current_data), 3)):
            print("---", current_data[n].name)
        # possible improvement = count children
        print(
            "*Vybral jsem \"{}\" protože je na nejvyšším místě v grafu ({}) a její zodpovězení může odebrat {} přímých nejasností." \
            .format(current_data[0].name, current_data[0].height, len(current_data[0].edges_out)))

    def _explain(self, solution):
        """
        Explain how i got to the current solution.
        """
        # Get the whole data
        whole_graph = ChatBot()

        # all nodes that were marked as true either by user or implied
        all_true = self.implied_true.union(self.answered_true).union(self.current_subgraph)

        # get the nodes that were not used
        unused = all_true.symmetric_difference(whole_graph.data_graph.nodes)

        # remove the unused nodes from graph
        whole_graph.data_graph.remove_nodes(unused)

        return [solution, whole_graph]

    def _final_explain(self, deep=False):
        if not deep:
            response = self._post_question("Zobrazit všecha řešení " + str(len(self.explanations)) + " řešení? [y/*]: ")
            if response == "y":
                limit = len(self.explanations)
                print("*Zobrazuji všech", len(self.explanations), "řešení.")
            else:
                limit = min(2, len(self.explanations))
                print("*Zobrazuji nejlepší", limit, "řešení.")
        else:
            limit = len(self.explanations)

        # sum all probabilities
        prob_sum = 0
        for i in range(0, len(self.explanations)):
            prob_sum += self.explanations[i][0].ziskej_finalni_pst()

        # add recalculated probabilities
        for i in range(0, len(self.explanations)):
            self.explanations[i].append(self.explanations[i][0].ziskej_finalni_pst() / prob_sum)

        # sort the recalculated probabilities
        self.explanations.sort(key=lambda x: x[2], reverse=True)

        # print all probabilities
        for i in range(0, limit):
            print("*Řešení", str(i) + ":", self.explanations[i][0].name, "s pravděpodobností:",
                  round(self.explanations[i][2], 5))

            if deep:
                # self.explanations[i][1].data_graph.graphviz_draw("Solution to:", self.explanations[i][0].name)
                self.explanations[i][1].data_graph.print_nice()

    def end_bot(self):
        self._final_explain()

        res = self._post_question("*Chceš vysvětlit, jak jsem došel k těmto závěrům? [y/*]: ")
        if res == "y":
            self._final_explain(deep=True)

    def ask(self):
        """
        On step of the knowledge bot. Ask the user and then parse the answer
        :return: True if ended
        :rtype: bool
        """
        # update the sources
        if len(self.current_subgraph) == 0:
            current_data = self._select_sources(self.data_graph.nodes)
        else:
            current_data = self._select_sources(self.current_subgraph)

        # ask for the node with the highest priority .. sorted by (height, num of outgoing edges)
        selected = current_data[0]
        response = self._post_question("Je pravda, že \"" + selected.name + "\"? [y/n/w/(0-1)]: ")

        # Check for numerical response
        response_num = None
        if response not in ["y", "w", "s", "n"]:
            try:
                response_num = float(response)

                if not (0 < response_num <= 1):
                    self._post_answer("*Zadané číslo není z intervalu (0, 1>.")
                    return False
            except ValueError:
                self._post_answer("*Neznámá odpověď.")
                return False

        """ Actions based on the response of the user: """
        if response == "y" or response_num is not None:
            # not defining value is like answering with 1
            if response_num is None:
                response_num = 1

            # specialize on the current subgraph
            self.current_subgraph = self.data_graph.get_subgraph(selected)
            implied = self.current_subgraph.copy()

            # check if this node led to a solution
            solution = selected.get_solution()
            if solution is not None:
                print("*Found a solution", solution.name)
                self.explanations.append(self._explain(solution))

            # traverse the graph and remove all descendants which do not rely only on this node
            self.data_graph.remove_node_and_descendants(node=selected, ancestors=False, direct=True, node_from=None,
                                                        user_prob=response_num)

            # remove current node and all implied descendants from the subgraph
            intersection = self.current_subgraph.intersection(self.data_graph.nodes)
            self.current_subgraph = intersection

            # add the implied nodes and the answered node
            if solution is None:
                implied = implied.symmetric_difference(self.current_subgraph)
                implied.remove(selected)
                self.answered_true.add(selected)
                self.implied_true = self.implied_true.union(implied)

            if len(self.current_subgraph) == 0 and len(self.data_graph.nodes) == 0:
                self.end_bot()
                return True

        elif response == "n":
            # remove only the
            self.data_graph.remove_node_and_descendants(node=selected, ancestors=True, direct=False, node_from=None, user_prob=None)

            # update the currently selected set to reflect the removed nodes
            self.current_subgraph = self.current_subgraph.intersection(self.data_graph.nodes)

            # check if there are any nodes left in the graph
            if len(self.data_graph.nodes) == 0:
                if len(self.explanations) == 0:
                    self._post_answer("*Neznám řešení tvého problému.")
                else:
                    self.end_bot()
                return True

        elif response == "w":
            self._why(current_data)

        elif response == "s":
            self.data_graph.graphviz_draw()

        else:
            self._post_answer("*Neznámá odpověď.")

        return False


if __name__ == "__main__":
    print("*Bayesův znalostní systém opraváře kol nastartován.")

    try:
        c = ChatBot()
    except Exception as e:
        print("*Inicialization of the chatbot failed with the error of:", str(e))
        exit(0)

    while not c.ask():
        pass

    print("*Konec programu.")
