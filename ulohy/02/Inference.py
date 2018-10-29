from Graph.Graph import Graph


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


    def _load_data(self):
        """
        Load the data from the knowledge base file and parse the clausules.
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
                solution = separated[1]
                for cond in conditions:
                    data_graph.add_edge(cond.strip(), solution.strip(), "")
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

        node_sources.sort(reverse=True, key=lambda n: (len(n.edges_out), n.height))
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
        return input(question)

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
        print("jsou celkem {} otázky, které mohou pomoci posunout se dál. Top {} z nich jsou: "\
            .format(len(current_data), min(len(current_data), 3)))
        for n in range(0, min(len(current_data), 3)):
            print("-", current_data[n].name)
        # possible improvement = count children
        print("Vybral jsem \"{}\" protože je na nejvyšším místě v grafu ({}) a její zodpovězení může odebrat {} přímých nejasností."\
            .format(current_data[0].name, current_data[0].height, len(current_data[0].edges_out)))

    def _explain(self, solution):
        """
        Explain how i got to the current solution.
        """
        all_true = self.implied_true.union(self.answered_true).union(self.current_subgraph)

        # recalculate all data
        self.data_graph = self._initialise_data()

        # get the nodes that were not used
        unused = all_true.symmetric_difference(self.data_graph.nodes)

        # remove the unused nodes from graph
        self.data_graph.remove_nodes(unused)

        # print the remaining graph:
        print("Řešení bylo odvozeno od následujícího průchodu grafem: ")
        self.data_graph.graphviz_draw("Solution to:", solution.name)
        self.data_graph.print_nice()

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
        response = self._post_question("Je pravda, že \"" + selected.name + "\"? [y/n/w]: ")

        """ Actions based on the response of the user: """
        if response == "y":
            # specialize on the current subgraph
            self.current_subgraph = self.data_graph.get_subgraph(selected)
            implied = self.current_subgraph.copy()

            # check if this node led to a solution
            solution = selected.get_solution()
            if solution is not None:
                print("Řešení:", solution.name)
                response = self._post_question("Chceš vysvětlit proč? [y/*]: ")
                if response == "y":
                    self._explain(solution)
                return True

            # traverse the graph and remove all descendants which do not rely only on this node
            self.data_graph.remove_node_and_descendants(selected, ancestors=False, direct=True)

            # remove current node and all implied descendants from the subgraph
            intersection = self.current_subgraph.intersection(self.data_graph.nodes)
            self.current_subgraph = intersection

            # delete all remaining nodes that are not in the current subgraph from the whole graph
            diff = self.data_graph.nodes.difference(self.current_subgraph)
            self.data_graph.remove_nodes(diff)

            # add the implied nodes and the answered node
            implied = implied.symmetric_difference(self.current_subgraph)
            implied.remove(selected)
            self.answered_true.add(selected)
            self.implied_true = self.implied_true.union(implied)

        elif response == "n":
            # remove only the
            self.data_graph.remove_node_and_descendants(selected, ancestors=True, direct=False)

            # update the currently selected set to reflect the removed nodes
            self.current_subgraph = self.current_subgraph.intersection(self.data_graph.nodes)

            # check if there are any nodes left in the graph
            if len(self.data_graph.nodes) == 0:
                self._post_answer("Neznám řešení tvého problému.")
                return True

        elif response == "w":
            self._why(current_data)

        else:
            self._post_answer("Neznámá odpověď.")

        return False


if __name__ == "__main__":
    """
    Run the bot. 
    """
    print("Znalostní systém opraváře kol nastartován.")

    c = ChatBot()
    # c.data_graph.graphviz_draw()

    while not c.ask():
        pass
        # c.data_graph.graphviz_draw()

    print("Konec programu.")

