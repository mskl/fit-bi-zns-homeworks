from Graph.Graph import Graph

if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("D", "B")
    g.add_edge("F", "D")
    g.add_edge("E", "D")
    g.add_edge("D", "Z")

    g.calculate_max_heights()

    #g.remove_node("F")
    #g.remove_node_and_descendants("D")

    #print(g.get_subgraph("A"))

    # print(g)
    #print(g.get_node_from_string("A").edges_in)
    #print(g.get_node_from_string("A").edges_out)

    g.graphviz_draw()
