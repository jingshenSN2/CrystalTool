import networkx as nx
import matplotlib.pyplot as plt


def graph_converter(cell):
    g = nx.Graph()
    for atom in cell.atom_list:
        g.add_node(atom, location=(atom.x, atom.y), label=atom.element + atom.index)
        for neighbor in atom.neighbors.keys():
            if (atom, neighbor) not in g.edges:
                g.add_edge(atom, neighbor, dist=round(atom.neighbors[neighbor], 2))
    return g


def max_subgraph(graph):
    c = max(nx.connected_components(graph), key=len)
    return graph.subgraph(c)


def draw_graph(graph):
    plt.figure(figsize=(10, 9))
    pos = nx.get_node_attributes(graph, 'location')
    label = nx.get_node_attributes(graph, 'label')
    edge_label = nx.get_edge_attributes(graph, 'dist')
    nx.draw_networkx(graph, pos, alpha=0.7, with_labels=False, edge_color='.4')
    nx.draw_networkx_labels(graph, pos, labels=label)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_label)
    plt.axis('off')
    plt.tight_layout()
    plt.show()