graph_style = {
    'graph': {
        #'nodesep': '0',
    },
    'nodes': {
        'fontname': 'Helvetica',
    },
    'edges': {
        # 'dir': 'none',
        #'len': '10',
        #'weight': '10'
    }
}


def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles[ 'graph' ]) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles[ 'nodes' ]) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles[ 'edges' ]) or {}
    )
    return graph