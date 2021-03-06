graph_style = {
    'graph': {
        # 'nodesep': '0',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'egg'
    },
    'edges': {
        # 'dir': 'none',
        # 'len': '10',
        # 'weight': '10'
    }
}


def apply_styles(graph, styles):
    """
    Apply all styles that graphviz has at once.
    :param graph: target graphviz graph
    :param styles: style dict
    :type styles: dict
    :return: graphviz graph with applied styles
    """
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph
