from Graph.Graph import Graph


class ChatBot:
    def __init__(self):
        # load and classify data
        self.data_graph = self.load_data()
        self.data_graph.calculate_max_heights()

        self.messages_sent = []
        self.messages_received = []
        self.node_sources = []

        self.current_subgraph = set()

    def load_data(self):
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

    def process_data(self, nodes):
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

        node_sources.sort(reverse=True, key=lambda n: (n.height, len(n.edges_in)))
        return node_sources

    def _post_question(self, question):
        self.messages_sent.append(question)
        return input(question)

    def _post_answer(self, answer):
        print(answer)
        self.messages_received.append(answer)

    def ask(self):
        # update the sources
        if len(self.current_subgraph) == 0:
            current_data = self.process_data(self.data_graph.nodes)
        else:
            current_data = self.process_data(self.current_subgraph)

        # keep asking for the highest priority sources
        selected = current_data[0]
        response = self._post_question("Je pravda, že \"" + selected.name + "\"? [y/n]: ")

        if response == "y":
            # specialize on the current subgraph
            self.current_subgraph = self.data_graph.get_subgraph(selected)

            # check if this node led to a solution
            solution = selected.get_solution()
            if solution is not None:
                print("Řešení:", solution.name)
                return True

            # remove currently asked node
            self.data_graph.remove_node_and_descendants(selected, ancestors=False, direct=True)

            # remove current node from the subgraph set as well
            self.current_subgraph = self.current_subgraph.intersection(self.data_graph.nodes)

            # delete all remaining nodes that are not in the current subgraph
            diff = self.data_graph.nodes.difference(self.current_subgraph)
            self.data_graph.remove_nodes(diff)

        elif response == "n":
            # delete all descendants
            self.data_graph.remove_node_and_descendants(selected, ancestors=True, direct=False)
            # update the currently selected set to reflect the removed nodes
            self.current_subgraph = self.current_subgraph.intersection(self.data_graph.nodes)
            # check if there are any nodes left in the graph
            if len(self.data_graph.nodes) == 0:
                self._post_answer("Neznám řešení tvého problému.")
                return True

        else:
            self._post_answer("Neznámá odpověď.")

        return False


if __name__ == "__main__":
    c = ChatBot()
    print("Znalostní systém opraváře kol nastartován.")
    c.data_graph.graphviz_draw()

    # Keep asking until I have an answer
    while not c.ask():
        c.data_graph.graphviz_draw()

    print("Konec programu.")

