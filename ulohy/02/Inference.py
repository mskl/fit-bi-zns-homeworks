from Graph.Graph import Graph


class ChatBot:
    messages = []

    node_outgoing = []
    node_incoming = []

    node_true = set()
    node_false = set()

    data_graph = None

    def __init__(self):
        self.load_data()
        self.process_data()
        self.data_graph.graphviz_draw()

    def load_data(self):
        with open("znalostni_baze.txt") as f:
            content = f.readlines()

        self.data_graph = Graph("Expertní systém opraváře kol")
        for line in content:
            separated = line.strip(" IF ").split(" THEN ")
            if len(separated) == 2:
                conditions = separated[0].split("AND")
                solution = separated[1]
                for cond in conditions:
                    self.data_graph.add_edge(cond.strip(), solution.strip(), "")

    def process_data(self):
        for node in self.data_graph.get_nodes():
            o = i = 0
            for e in node.get_edges():
                if e.from_node(node):
                    o += 1
                elif e.to_node(node):
                    i += 1
            self.node_incoming.append((i, node))
            self.node_outgoing.append((o, node))

        self.node_outgoing.sort(reverse=True, key=lambda x: x[0])
        self.node_incoming.sort(reverse=True, key=lambda x: x[0])

    def ask(self):
        selected = None
        for n in self.node_outgoing:
            # todo remove unreachable nodes..
            if n[1] not in self.node_true and n[1] not in self.node_false:
                selected = n[1]
                break

        response = input("Tvoje odpověď na " + selected.get_name() + "[y/n]: ")
        self.messages.append(response)
        if response == "y":
            self.node_true.add(selected)
        else:
            self.node_false.add(selected)


if __name__ == "__main__":
    c = ChatBot()

    while True:
        c.ask()
