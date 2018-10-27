from Graph.Graph import Graph

if __name__ == "__main__":
    with open("baze.txt") as f:
        content = f.readlines()

    g = Graph("Expertní systém opraváře kol")
    for line in content:
        # Parse the line
        separated = line.strip(" IF ").split(" THEN ")
        if len(separated) == 2:
            conditions = separated[0].split("AND")
            solution = separated[1]
            for c in conditions:
                g.add_edge(solution.strip(), c.strip(), "")

    g.graphviz_draw(view=True)

